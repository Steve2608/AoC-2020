# include <stdio.h>
# include <stdlib.h>
# include "../util.c"

# define ARR_SIZE 200

int part1(struct int_array* data, int target) {
    int* vals = data->data;
    for (int i = 0; i < data->len; i++) {
        for (int j = 0; j < data->len; j++) {
            if (vals[i] + vals[j] == target) {
                return vals[i] * vals[j];
            }
        }
    }
    return -1;
}

int part2(struct int_array* data, int target) {
    int* vals = data->data;
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
    struct int_array* data = read_input_int_array("01/input.txt", ARR_SIZE);
    if (data == NULL) {
        exit(EXIT_FAILURE);
    }

    int p1 = part1(data, 2020);
    printf("part1: %d\n", p1);

    int p2 = part2(data, 2020);
    printf("part2: %d\n", p2);

    free(data->data);
    free(data);

    exit(EXIT_SUCCESS);
}
