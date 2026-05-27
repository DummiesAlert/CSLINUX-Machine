//Question 3:

#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

typedef struct {
    int *array;
    int size; 
} ThreadData;

void sort_array(int *arr, int size) {
    for (int i = 0; i < size - 1; i++) {
        for (int j = i + 1; j < size; j++) {
            if (arr[i] > arr[j]) {
                int temp = arr[i];
                arr[i] = arr[j];
                arr[j] = temp;
            }
        }
    }
}

void *worker(void *arg) {
    ThreadData *data = (ThreadData *)arg;
    sort_array(data->array, data->size);
    return NULL;
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Error: Please provide a list of numbers.\n");
        return 1;
    }

    int total_elements = argc - 1;
    int *full_array = malloc(total_elements * sizeof(int));

    for (int i = 0; i < total_elements; i++) {
        full_array[i] = atoi(argv[i + 1]);
    }

    int mid = total_elements / 2;
    int size1 = mid;
    int size2 = total_elements - mid;

    ThreadData thread1_data = { &full_array[0], size1 };
    ThreadData thread2_data = { &full_array[mid], size2 };

    pthread_t thread1, thread2;

    pthread_create(&thread1, NULL, worker, (void *)&thread1_data);
    pthread_create(&thread2, NULL, worker, (void *)&thread2_data);

    pthread_join(thread1, NULL);
    pthread_join(thread2, NULL);

    int *merged_array = malloc(total_elements * sizeof(int));
    int i = 0, j = mid, k = 0;

    while (i < mid && j < total_elements) {
        if (full_array[i] <= full_array[j]) {
            merged_array[k++] = full_array[i++];
        } else {
            merged_array[k++] = full_array[j++];
        }
    }

    while (i < mid) {
        merged_array[k++] = full_array[i++];
    }

    while (j < total_elements) {
        merged_array[k++] = full_array[j++];
    }

    printf("Sorted array: ");
    for (int idx = 0; idx < total_elements; idx++) {
        printf("%d ", merged_array[idx]);
    }
    printf("\n");

    free(full_array);
    free(merged_array);

    return 0;
}
