#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <ctype.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <errno.h>
#include <string.h>
#include <time.h>
#include <vector>
#define MAX_SIZE 12

int process_stream(int input_port, int output_port);

int main(int argc, char* argv[])
{
    if (argc < 3)
    {
        printf("Need input and output streams ports as parameters!\n");
        return -1;
    }

    int input_port = atoi(argv[1]);
    int output_port = atoi(argv[2]);

    for (;;) // forever and ever
    {
        printf("I am waiting for a Matrix at port %d\n", input_port);
        process_stream(input_port, output_port);
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

float get_line_avg(std::vector<float> line)
{
    int count = line.size();
    float sum = 0;

    for (int i = 0; i < count; i++)
        sum += line[i] / count;

    return sum;
}

std::vector<char> get_avg_vector(std::vector<std::vector<float>> matrix)
{
    std::vector<float> result;
    
    int matrix_size = matrix.size();

    result.reserve(matrix_size);

    for (int i = 0; i < matrix_size; i++) 
    {
        double avg = get_line_avg(matrix[i]);
        result[i] = avg;
    }

    std::vector<char> char_result;

    for (int i = 0; i < matrix_size; i++) 
    {
        char* avg_str = new char[MAX_SIZE];
        sprintf(avg_str, "%.8f ", result[i]);
        char_result.insert(char_result.end(), avg_str, avg_str + strlen(avg_str));
    }

    char_result.push_back('\n');

    return char_result;
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

int process_stream(int input_port, int output_port)
{
    int* connection = listen_to_port(input_port);

    std::vector<std::vector<float>> matrix;

    int stream_size = get_stream_matrix(connection[0], matrix);

    close_connection(connection[0], connection[1]);

    double start = getMilliseconds();

    std::vector<char> result = get_avg_vector(matrix);

    double end = getMilliseconds();
    double execution_time_in_seconds = (double)(end - start);

    char* buffer = new char[256];
    sprintf(buffer, "%d bytes in %.9f milliseconds\n", stream_size, execution_time_in_seconds);

    result.insert(result.end(), buffer, buffer + strlen(buffer));
    result.push_back('\0');

    send_stream_to_port(output_port, &result[0]);

    return 0;
}