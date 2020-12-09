#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <ctype.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <errno.h>
#include <string.h>
#include <vector>
#include <time.h>
// CUDA runtime
#include <cuda_runtime.h>
// helper functions and utilities to work with CUDA
#include <helper_functions.h>
#include <helper_cuda.h>
#define MAX_SIZE 12

int process_stream(int input_port, int output_port, int devId);

int main(int argc, char* argv[])
{
    if (argc < 3)
    {
        printf("Need input and output streams ports as parameters!\n");
        return -1;
    }

    int input_port = atoi(argv[1]);
    int output_port = atoi(argv[2]);

    int devId = findCudaDevice(argc, (const char **)argv);

    for (;;) // forever and ever
    {
        printf("I am waiting for a Matrix at port %d\n", input_port);
        process_stream(input_port, output_port, devId);
    }

    return 0;
}

double getMilliseconds() {
    return 1000.0 * clock() / CLOCKS_PER_SEC;
}

int* listen_to_port(int port)
{
    int sfd, connection;

    int* opts = new int[1]{ 1 };

    if ((sfd = socket(AF_INET, SOCK_STREAM, 0)) == 0
        || setsockopt(sfd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, opts, sizeof(int)))
    {
        printf("%s\n", strerror(errno));
        exit(EXIT_FAILURE);
    }

    struct sockaddr_in address;
    int addrlen = sizeof(address);
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(port);

    if (bind(sfd, (struct sockaddr*)&address,
        sizeof(address)) < 0 || listen(sfd, 3) < 0
        || (connection = accept(sfd, (struct sockaddr*)&address, (socklen_t*)&addrlen)) < 0)
    {
        printf("%s\n", strerror(errno));
        exit(EXIT_FAILURE);
    }

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
    {
        printf("%s\n", strerror(errno));
        exit(EXIT_FAILURE);
    }

    struct sockaddr_in serv_addr;
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = INADDR_ANY;
    serv_addr.sin_port = htons(port);

    if (connect(sock, (struct sockaddr*)&serv_addr, sizeof(serv_addr)) < 0)
    {
        printf("%s\n", strerror(errno));
        exit(EXIT_FAILURE);
    }

    send(sock, stream, strlen(stream), 0);

    shutdown(sock, SHUT_WR);
    close(sock);
}

int get_stream_matrix(int connection, std::vector<std::vector<float>> &matrix)
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

void convertVectorToFlatArray(std::vector<std::vector<float>> matrix, float *flat)
{
    int msize = matrix.size();
    for (int i = 0; i < msize; i++)
    { 
        for (int j = 0; j < msize; j++)
        {
            flat[j + (i * msize)] = matrix[i][j];
        }
    }
 }

__global__ void get_avg_vector(float *matrix, float *result, int n)
{
    int row_idx = blockIdx.x * blockDim.x + threadIdx.x;
    int nsqrd = n*n;

    if (row_idx < nsqrd)
    {
        for (int i = row_idx; i < nsqrd; i += blockDim.x * gridDim.x)
            atomicAdd(&result[i / n], matrix[i] / n);
    }
    
}

int process_stream(int input_port, int output_port, int devId)
{
    int* connection = listen_to_port(input_port);

    std::vector<std::vector<float>> matrix;

    int stream_size = get_stream_matrix(connection[0], matrix);

    close_connection(connection[0], connection[1]);

    int matrix_size = matrix.size();
    int row_size = matrix_size * sizeof(float);
    int flat_size = matrix_size * matrix_size * sizeof(float);

    float *a_matrix = (float*)malloc(flat_size);
    convertVectorToFlatArray(matrix, a_matrix);

    float *d_matrix;
    float *d_result;

    cudaMalloc(&d_matrix, flat_size);
    cudaMemcpy(d_matrix, a_matrix, flat_size, cudaMemcpyHostToDevice);
    
    cudaMalloc(&d_result, row_size);
    cudaMemset(d_result, 0, row_size);

    int numSMs;
    cudaDeviceGetAttribute(&numSMs, cudaDevAttrMultiProcessorCount, devId);

    cudaDeviceProp props;
    cudaGetDeviceProperties(&props, devId);
    printf("Executed on device \"%s\"\n", props.name);

    double start = getMilliseconds();

    get_avg_vector<<<numSMs, 256>>>(d_matrix, d_result, matrix_size);

    double end = getMilliseconds();
    double execution_time_in_seconds = (double)(end - start);

    float *float_result = (float*)malloc(row_size);
    cudaMemcpy(float_result, d_result, row_size, cudaMemcpyDeviceToHost);

    std::vector<char> result;

    for (int i = 0; i < matrix_size; i++) 
    {
        char* avg_str = new char[MAX_SIZE];
        sprintf(avg_str, "%.8f ", float_result[i]);
        result.insert(result.end(), avg_str, avg_str + strlen(avg_str));
    }
    result.push_back('\n');

    char* buffer = new char[256];
    sprintf(buffer, "%d bytes in %.9f milliseconds\n", stream_size, execution_time_in_seconds);

    result.insert(result.end(), buffer, buffer + strlen(buffer));
    result.push_back('\0');

    send_stream_to_port(output_port, &result[0]);

    cudaFree(d_result);
    cudaFree(d_matrix);
    free(float_result);
    free(a_matrix);

    return 0;
}