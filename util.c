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

void free_long_array(struct long_array* data) {
    if (data != NULL) {
        free(data->data);
    }
    free(data);
}

struct int_array {
    int* data;
    size_t len;
};

struct int_array* read_input_int_array(const char* file_name, const size_t input_len) {
    struct int_array* res;

    FILE* fp = fopen(file_name, "r");
    if (fp == NULL) {
        perror(file_name);
        return NULL;
    }

    int* data = malloc(sizeof(int) * input_len);
    size_t len = 0;

    int val;
    while (!feof(fp)) {
        if (fscanf(fp, "%d", &val) >= 1) {
            data[len++] = val;
        }
    }
    fclose(fp);

    res = malloc(sizeof(struct int_array));
    res->data = data;
    res->len = len;
    return res;
}

void free_int_array(struct int_array* data) {
    if (data != NULL) {
        free(data->data);
    }
    free(data);
}