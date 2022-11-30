# include <stdio.h>
# include <stdlib.h>
# include "../util.c"

# define ARR_SIZE 200

long part1(struct long_array* data, long target) {
    long* vals = data->data;
    for (int i = 0; i < data->len; i++) {
        for (int j = 0; j < data->len; j++) {
            if (vals[i] + vals[j] == target) {
                return vals[i] * vals[j];
            }
        }
    }
    return -1;
}

long part2(struct long_array* data, long target) {
    long* vals = data->data;
    for (int i = 0; i < data->len; i++) {
        for (int j = 0; j < data->len; j++) {
            for (int k = 0; k < data->len; k++) {
                if (vals[i] + vals[j] + vals[k] == target) {
                    return vals[i] * vals[j] * vals[k];
                }
            }
        }
    }
    return -1;
}

int main() {
    struct long_array* data = read_input_long_array("01/input.txt", ARR_SIZE);
    if (data == NULL) {
        exit(EXIT_FAILURE);
    }

    long p1 = part1(data, 2020);
    printf("part1: %ld\n", p1);

    long p2 = part2(data, 2020);
    printf("part2: %ld\n", p2);

    free(data->data);
    free(data);

    exit(EXIT_SUCCESS);
}