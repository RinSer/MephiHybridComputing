#include <cstdio>
#include <cstdlib>
#include <ctype.h>
#include <string.h>
#include <time.h>

int process_file(char* file_path, FILE* out_file);
double getMilliseconds();

int main()
{
    FILE* out = fopen("result.txt", "w");
    
    double start = getMilliseconds();

    char input_path[9];
    int size = 1000;
    while (size < 16001)
    {
        sprintf(input_path, "%d.txt", size);
        process_file(input_path, out);
        size *= 2;
    }

    double end = getMilliseconds();
    double total_execution_time_in_seconds = (double)(end - start);
    fprintf(out, "Total execution time: %.3f milliseconds", total_execution_time_in_seconds);

    fclose(out);

    return 0;
}

double getMilliseconds() {
    return 1000.0 * clock() / CLOCKS_PER_SEC;
}

void trim_str(char* str)
{
    for (int i = 0; i < strlen(str); i++)
    {
        if (!isdigit(str[i]))
        {
            str[i] = NULL;
            return;
        }
    }
}

long fsize(FILE* fp) {
    int initial = ftell(fp);

    fseek(fp, 0, SEEK_END);

    long size = ftell(fp);

    fseek(fp, initial, SEEK_SET);

    return size;
}

float get_line_avg(char* line)
{
    int count = 0;
    int sum = 0;
    char* number = strtok(line, " ");

    while (number != NULL)
    {
        trim_str(number);
        sum += atoi(number);
        count++;
        number = strtok(NULL, " ");
    }

    return (float)sum / count;
}

char* get_file_vector(FILE* fp, long size)
{
    char* result = new char[size];
    char* line = NULL;
    size_t len = 0;

    while ((getline(&line, &len, fp)) != -1)
    {
        float avg = get_line_avg(line);
        char* avg_str = new char[size];
        sprintf(avg_str, "%f", avg);
        strcat(strcat(result, avg_str), " ");
    }

    return result;
}

int process_file(char* file_path, FILE* out_file)
{
    double start = getMilliseconds();

    FILE* fp = fopen(file_path, "r");
    if (fp == NULL)
        exit(EXIT_FAILURE);

    long file_size = fsize(fp);

    char* result = get_file_vector(fp, file_size);

    fclose(fp);

    fprintf(out_file, "%s\n", result);

    double end = getMilliseconds();
    double execution_time_in_seconds = (double)(end - start);
    printf("%d bytes in %.3f milliseconds\n", file_size, execution_time_in_seconds);

    fprintf(out_file, "%d bytes in %.3f milliseconds\n", file_size, execution_time_in_seconds);

    return 0;
}