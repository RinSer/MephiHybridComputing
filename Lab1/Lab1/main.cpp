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
#define MAX_SIZE 12

int process_stream(int input_port, int output_port);

int main(int argc, char* argv[])
{
    if (argc < 3)
    {
        printf("Need input and output streams ports as parameters!");
        return -1;
    }

    int input_port = atoi(argv[1]);
    int output_port = atoi(argv[2]);

    for (;;) // forever and ever
    {
        #pragma omp parallel
        #pragma omp single
        {
            process_stream(input_port, output_port);
        }
    }

    return 0;
}

double getMilliseconds() {
    return 1000.0 * clock() / CLOCKS_PER_SEC;
}

void trim_str(char* str)
{
    for (int i = 0; i < strlen(str); i++)
    {
        if (!isdigit(str[i]) && str[i] != '.')
        {
            str[i] = NULL;
            return;
        }
    }
}

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

double get_line_avg(char* line)
{
    int count = 0;
    double sum = 0;
    char* number = strtok(line, " ");

    while (number != NULL)
    {
        trim_str(number);
        sum += atof(number);
        count++;
        number = strtok(NULL, " ");
    }

    return (double)sum / count;
}

int get_stream_vector(int connection, std::vector<char> &result)
{
    int buffer_size = 1;
    char* buffer = new char[buffer_size];
    
    int line_count = -1;
    int stream_size = 0;
    while (read(connection, buffer, buffer_size) > 0)
    {
        stream_size++;
        int num_bytes = 1;

        std::vector<char> line;

        while (buffer[0] != '\n' && num_bytes > 0)
        {
            line.push_back(buffer[0]);
            num_bytes = read(connection, buffer, buffer_size);
            stream_size++;
        }
        line.push_back(NULL);

        line_count++;

        #pragma omp task shared(result)
        {
            int current_line = line_count;
            double avg = get_line_avg(&line[0]);
            char* avg_str = new char[MAX_SIZE];
            sprintf(avg_str, "%.8f ", avg);

            #pragma omp critical
            result.insert(result.begin() + current_line * strlen(avg_str), avg_str, avg_str + strlen(avg_str));
        }
    }

    #pragma omp taskwait
    result.push_back('\n');

    return stream_size;
}

int process_stream(int input_port, int output_port)
{
    double start = getMilliseconds();

    int* connection = listen_to_port(input_port);

    std::vector<char> result;

    int stream_size = get_stream_vector(connection[0], result);

    close_connection(connection[0], connection[1]);

    char* buffer = new char[256];
    double end = getMilliseconds();
    double execution_time_in_seconds = (double)(end - start);
    sprintf(buffer, "%d bytes in %.3f milliseconds\n", stream_size, execution_time_in_seconds);

    result.insert(result.end(), buffer, buffer + strlen(buffer));
    result.push_back(NULL);

    send_stream_to_port(output_port, &result[0]);

    return 0;
}