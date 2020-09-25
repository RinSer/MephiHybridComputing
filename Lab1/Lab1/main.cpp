#include <cstdio>
#include <cstdlib>
#include <ctype.h>
#include <string.h>
#include <time.h>

int process_file(char* file_path, FILE* out_file);
double getMilliseconds();

int main(int argc, char* argv[])
{
    if (argc < 3)
    {
        printf("Need input file path and output file path arguments!");
        return -1;
    }
    
    FILE* out = fopen(argv[2], "w");
    
    double start = getMilliseconds();

    process_file(argv[1], out);

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
        if (!isdigit(str[i]) && str[i] != '.')
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

char* get_file_vector(FILE* fp, long size)
{
    char* result = new char[size];
    char* line = NULL;
    size_t len = 0;

    while ((getline(&line, &len, fp)) != -1)
    {
        double avg = get_line_avg(line);
        char* avg_str = new char[size];
        sprintf(avg_str, "%.8f", avg);
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