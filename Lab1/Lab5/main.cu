#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <ctype.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <string.h>
#include <time.h>
#include <vector>
#include <math.h>
#include <mpi.h>
// CUDA runtime
#include <cuda_runtime.h>
// helper functions and utilities to work with CUDA
#include <helper_functions.h>
#include <helper_cuda.h>

#define WORD_SIZE 11
#define MAX_SIZE 12

int* listen_to_port(int port)
{
    int sfd, connection;

    int* opts = new int[1]{ 1 };

    if ((sfd = socket(AF_INET, SOCK_STREAM, 0)) == 0
        || setsockopt(sfd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, opts, sizeof(int)))
        exit(EXIT_FAILURE);

    struct sockaddr_in address;
    int addrlen = sizeof(address);
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(port);

    if (bind(sfd, (struct sockaddr*)&address,
        sizeof(address)) < 0 || listen(sfd, 3) < 0
        || (connection = accept(sfd, (struct sockaddr*)&address, (socklen_t*)&addrlen)) < 0)
        exit(EXIT_FAILURE);

    return new int[2]{ connection, sfd };
}

void close_connection(int connection, int sfd)
{
    shutdown(connection, SHUT_RDWR);
    close(connection);
    shutdown(sfd, SHUT_RDWR);
    close(sfd);
}

void send_stream_to_port(int port, char* stream)
{
    int sock = 0;
    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0)
        exit(EXIT_FAILURE);

    struct sockaddr_in serv_addr;
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = INADDR_ANY;
    serv_addr.sin_port = htons(port);

    if (connect(sock, (struct sockaddr*)&serv_addr, sizeof(serv_addr)) < 0)
        exit(EXIT_FAILURE);

    send(sock, stream, strlen(stream), 0);

    shutdown(sock, SHUT_WR);
    close(sock);
}

int get_stream_matrix(int connection, std::vector<std::vector<float>>& matrix)
{
    int buffer_size = 1;
    char* buffer = new char[buffer_size];

    std::vector<char> number;
    std::vector<float> line;
    int stream_size = 0;
    while (read(connection, buffer, buffer_size) > 0)
    {
        stream_size++;
        int num_bytes = 1;

        while (buffer[0] != '\n' && num_bytes > 0)
        {
            if (buffer[0] == ' ')
            {
                line.push_back(atof(&number[0]));
                number.clear();
            }
            else
                number.push_back(buffer[0]);

            num_bytes = read(connection, buffer, buffer_size);
            stream_size++;
        }
        line.push_back(atof(&number[0]));
        number.clear();

        matrix.push_back(line);

        line.clear();
    }

    return stream_size;
}

__global__ void get_avg_vector(float *matrix, float *result, int row_size, int num_rows)
{
    int row_idx = blockIdx.x * blockDim.x + threadIdx.x;
    int max_idx = row_size * num_rows;

    if (row_idx < max_idx)
    {
        for (int i = row_idx; i < max_idx; i += blockDim.x * gridDim.x) 
        {
            atomicAdd(&result[i / row_size], matrix[i] / row_size);
        }
    }
}

int main(int argc, char* argv[])
{
    if (argc < 3)
    {
        printf("Need input and output streams ports as parameters!");
        return -1;
    }

    int input_port = atoi(argv[1]);
    int output_port = atoi(argv[2]);

    int devId = findCudaDevice(argc, (const char **)argv);

    MPI_Init(&argc, &argv);

    for (;;) // forever and ever
    {
        int rank, numtasks, stream_size, num_elements, row_size;

        std::vector<std::vector<float>> matrix;
        std::vector<float> flat_matrix;
        std::vector<float> matrix_row;

        MPI_Comm_rank(MPI_COMM_WORLD, &rank);
        MPI_Comm_size(MPI_COMM_WORLD, &numtasks);

        int* sendcounts = new int[numtasks];
        int* displs = new int[numtasks];

        if (rank == 0) // only the first process communicates with external
        {
            int* connection = listen_to_port(input_port);

            stream_size = get_stream_matrix(connection[0], matrix);

            close_connection(connection[0], connection[1]);

            int total_size = matrix.size() * matrix.size();
            
            for (int i = 0; i < matrix.size(); i++)
                for (int j = 0; j < matrix[i].size(); j++)
                    flat_matrix.push_back(matrix[i][j]);

            row_size = (int)matrix.size();
            num_elements = (int)floor(total_size / numtasks);
            num_elements -= num_elements % row_size;

            // calculate send counts and displacements
            int sum = 0;
            for (int i = 0; i < numtasks; i++) {
                sendcounts[i] = num_elements;

                if (i == numtasks - 1)
                    sendcounts[i] = total_size - sum;

                displs[i] = sum;
                sum += sendcounts[i];
            }
        }

        MPI_Barrier(MPI_COMM_WORLD);

        MPI_Bcast(&num_elements, 1, MPI_INT, 0, MPI_COMM_WORLD);
        MPI_Bcast(&row_size, 1, MPI_INT, 0, MPI_COMM_WORLD);
        MPI_Bcast(sendcounts, numtasks, MPI_INT, 0, MPI_COMM_WORLD);
        MPI_Bcast(displs, numtasks, MPI_INT, 0, MPI_COMM_WORLD);

        int num_rows = sendcounts[rank] / row_size;

        std::vector<float> partial_matrix;
        partial_matrix.resize(row_size * row_size);

        double start;
        if (rank == 0) start = MPI_Wtime(); // only the first process controls the timing

        MPI_Scatterv(flat_matrix.data(), sendcounts, displs, MPI_FLOAT, partial_matrix.data(), sendcounts[numtasks-1], MPI_FLOAT, 0, MPI_COMM_WORLD);

        // CUDA kernel data initialization
        std::vector<float> lines_matrix = std::vector<float>(partial_matrix.begin(), partial_matrix.begin() + (num_rows * row_size));
        int matrix_size = lines_matrix.size();

        int row_float_size = num_rows * sizeof(float);
        int float_size = matrix_size * sizeof(float);

        float *a_matrix = (float*)malloc(float_size);
        for (int i = 0; i < matrix_size; i++)
            a_matrix[i] = lines_matrix[i];

        float *d_matrix;
        float *d_result;

        cudaMalloc(&d_matrix, float_size);
        cudaMemcpy(d_matrix, a_matrix, float_size, cudaMemcpyHostToDevice);
        
        cudaMalloc(&d_result, row_float_size);
        cudaMemset(d_result, 0, row_float_size);

        int numSMs;
        cudaDeviceGetAttribute(&numSMs, cudaDevAttrMultiProcessorCount, devId);

        cudaDeviceProp props;
        cudaGetDeviceProperties(&props, devId);

        get_avg_vector<<<numSMs, 256>>>(d_matrix, d_result, row_size, num_rows);

        float *float_result = (float*)malloc(row_float_size);
        cudaMemcpy(float_result, d_result, row_float_size, cudaMemcpyDeviceToHost);

        std::vector<char> partial_result;
        partial_result.reserve(num_rows);

        for (int i = 0; i < num_rows; i++) 
        {
            char* avg_str = new char[MAX_SIZE];
            sprintf(avg_str, "%.8f ", float_result[i]);
            partial_result.insert(partial_result.end(), avg_str, avg_str + strlen(avg_str));
        }

        cudaFree(d_result);
        cudaFree(d_matrix);
        free(float_result);
        free(a_matrix);

        // CUDA finished

        std::vector<char> parallel_result;
        if (rank == 0) parallel_result.reserve(WORD_SIZE * row_size);

        int* recvcounts = new int[numtasks];
        int* rdispls = new int[numtasks];
        int sum = 0;
        int char_size = num_elements / row_size * WORD_SIZE;
        for (int i = 0; i < numtasks; i++) {
            recvcounts[i] = char_size;

            if (i == numtasks - 1)
                recvcounts[i] = (row_size * WORD_SIZE) - sum;

            rdispls[i] = sum;
            sum += recvcounts[i];
        }

        MPI_Gatherv(partial_result.data(), (int)partial_result.size(), MPI_CHAR, parallel_result.data(), recvcounts, rdispls, MPI_CHAR, 0, MPI_COMM_WORLD);

        if (rank == 0) // only the first process communicates with external
        {
            char* result = new char[sum + 2];
            snprintf(result, sum + 1, "%s", &parallel_result[0]);
            
            double end = MPI_Wtime();
            double execution_time_in_seconds = (double)(end - start) * 1000;

            char* buffer = new char[sum + 3 + 256];
            snprintf(buffer, sum + 2 + 256, "%s\n%d bytes in %.9f milliseconds\n", result, stream_size, execution_time_in_seconds);
            printf("%s\n", buffer);

            send_stream_to_port(output_port, buffer);
        }
    }

    MPI_Finalize();

    return 0;
}