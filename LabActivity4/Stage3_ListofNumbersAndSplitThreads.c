// Write a C program which takes a list of numbers for its argument, it then splits that list in half and gives each half to a thread.
    // Within each thread, sort the numbers and return that to the main program. When both threads are finished, have the main program
    // combine the results to produce a single sorted list.

#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
typedef struct {
    int *array;
    int size;
}

ThreadNumbers;

void sortArray(int *arr, int size) {
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

void *threadWorkerrrrr(void *arg) {
    ThreadNumbers *numbers = (ThreadNumbers *)arg;
    sortArray(numbers->array, numbers->size);
    return NULL;
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Error: Invalid Arguments Given. It must be a list of numbers.\n");
        return 1;
    }

    int count = argc - 1;
    int *arrayAllocate = malloc(count * sizeof(int));

    for (int i = 0; i < count; i++) {
        arrayAllocate[i] = atoi(argv[i + 1]);
    }

    int arrayMiddle = count / 2;
    int size1 = arrayMiddle;
    int size2 = count - arrayMiddle;

    ThreadNumbers thread1 = { &arrayAllocate[0], size1};
    ThreadNumbers thread2 = { &arrayAllocate[arrayMiddle], size2};

    pthread_t thread1, thread2;

    pthread_create(&thread1, NULL, threadWorkerrrrr, (void *)&thread1);
    pthread_create(&thread2, NULL, threadWorkerrrrr, (void *)&thread2);

    pthread_join(thread1, NULL);
    pthread_join(thread2, NULL);

    int *sortedArray = malloc(count * sizeof(int));
    int i = 0, j = arrayMiddle, k = 0;

    while (i < arrayMiddle && j < count) {
        if (arrayAllocate[i] <= arrayAllocate[j]) {
            sortedArray[k++] = arrayAllocate[i++];
        } else {
            sortedArray[k++] = arrayAllocate[j++];
        }
    }

    while (i < arrayMiddle) {
        sortedArray[k++] = arrayAllocate[i++];
    }

    while (j < count) {
        sortedArray[k++] = arrayAllocate[j++];
    }

    printf("Sorted array: ");
    for (int m = 0; m < count; m++) {
        printf("%d ", sortedArray[m]);
    }
    printf("\n");

    free(arrayAllocate);
    free(sortedArray);

    return 0;
}
