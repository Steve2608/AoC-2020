# include <stdio.h>
# include <stdlib.h>

struct array_with_length {
    long* data;
    size_t len;
};

struct array_with_length* read_input(const char* file_name, const size_t input_len) {
    struct array_with_length* res;

    FILE* fp = fopen(file_name, "r");
    if (fp == NULL) {
        perror(file_name);
        return NULL;
    }

    long* data = malloc(sizeof(long) * input_len);
    size_t len = 0;

    long val;
    while (!feof(fp)) {
        if (fscanf(fp, "%ld", &val) >= 1) {
            data[len++] = val;
        }
    }
    fclose(fp);


    res = malloc(sizeof(struct array_with_length));
    res->data = data;
    res->len = len;
    return res;
}
