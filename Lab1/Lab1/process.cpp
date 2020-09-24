#include <cstdio>
#include <cstdlib>

int process_file(char* file_path)
{
    FILE* fp = fopen(file_path, "r");
    if (fp == NULL)
        exit(EXIT_FAILURE);

    char* line = NULL;
    size_t len = 0;
    while ((getline(&line, &len, fp)) != -1) {
        printf("%s", line);
    }

    fclose(fp);
    if (line)
        free(line);

    return 0;
}