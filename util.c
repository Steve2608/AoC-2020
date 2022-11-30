# include <stdio.h>
# include <stdlib.h>

struct long_array {
    long* data;
    size_t len;
};

struct long_array* read_input_long_array(const char* file_name, const size_t input_len) {
    struct long_array* res;

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

    res = malloc(sizeof(struct long_array));
    res->data = data;
    res->len = len;
    return res;
}
