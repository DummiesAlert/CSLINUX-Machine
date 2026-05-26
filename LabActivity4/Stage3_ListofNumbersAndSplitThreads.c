// Write a C program which takes a list of numbers for its argument, it then splits that list in half and gives each half to a thread.
    // Within each thread, sort the numbers and return that to the main program. When both threads are finished, have the main program
    // combine the results to produce a single sorted list. 

#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

typedef struct {
    int *array;
    int size;
} ThreadData;

// Sort function for each thread
void *sort_half(void *arg) {
    ThreadData *data = (ThreadData *)arg;

    // Simple bubble sort
    for (int i = 0; i < data->size - 1; i++) {
        for (int j = 0; j < data->size - i - 1; j++) {
            if (data->array[j] > data->array[j + 1]) {
                int temp = data->array[j];
                data->array[j] = data->array[j + 1];
                data->array[j + 1] = temp;
            }
        }
    }

    return NULL;
}

// Merge two sorted halves
void merge(int left[], int leftSize,
           int right[], int rightSize,
           int result[]) {

    int i = 0, j = 0, k = 0;

    while (i < leftSize && j < rightSize) {
        if (left[i] < right[j]) {
            result[k++] = left[i++];
        } else {
            result[k++] = right[j++];
        }
    }

    while (i < leftSize) {
        result[k++] = left[i++];
    }

    while (j < rightSize) {
        result[k++] = right[j++];
    }
}

int main(int argc, char *argv[]) {

    if (argc < 2) {
        printf("Usage: %s numbers...\n", argv[0]);
        return 1;
    }

    int total = argc - 1;

    int numbers[total];

    // Convert arguments to integers
    for (int i = 0; i < total; i++) {
        numbers[i] = atoi(argv[i + 1]);
    }

    // Split array in half
    int mid = total / 2;

    ThreadData firstHalf;
    firstHalf.array = numbers;
    firstHalf.size = mid;

    ThreadData secondHalf;
    secondHalf.array = numbers + mid;
    secondHalf.size = total - mid;

    pthread_t t1, t2;

    // Create threads
    pthread_create(&t1, NULL, sort_half, &firstHalf);
    pthread_create(&t2, NULL, sort_half, &secondHalf);

    // Wait for threads
    pthread_join(t1, NULL);
    pthread_join(t2, NULL);

    // Merge sorted halves
    int sorted[total];

    merge(firstHalf.array, firstHalf.size,
          secondHalf.array, secondHalf.size,
          sorted);

    // Print sorted array
    printf("Sorted list: ");

    for (int i = 0; i < total; i++) {
        printf("%d ", sorted[i]);
    }

    printf("\n");

    return 0;
}