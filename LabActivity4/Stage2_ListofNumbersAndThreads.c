// Write a C program which takes list of numbers (all less than 100) for its argument. Then it starts as many threads as there are numbers and in each
    // thread it counts down from the number given to 0, then ends.

// git pull origin main

#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

typedef struct {
    int threadNumber;
    int numbers;
}

ThreadNumbers;

void *countdown(void *arg) {
    ThreadNumbers * number = (ThreadNumbers *)arg;

    for (int i = number->numbers; i >= 0; i--) {
        printf("Thread %d: %d\n", number->threadNumber, i);
    }

    return NULL;
}
int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Usage of: %s, Is Invalid or No Arguments are provided\n", argv[0]);
        return 1;
    }

    int count = argc - 1;

    pthread_t threads[count];
    ThreadNumbers numbers[count];

    for (long i = 0; i < count; i++) {
        numbers[i].threadNumber = i;
        numbers[i].numbers = atoi(argv[i + 1]);

        if (numbers[i].numbers < 0 || numbers[i].numbers >= 100) {
            printf("Number is not less than 100! \nNumber: %d\n", numbers[i].numbers);
            return 1;
        }

        if (pthread_create(&threads[i], NULL, countdown, &numbers[i]) != 0) {
            perror("pthread_create");
            return 1;
        }
    }

    for (long i = 0; i < count; i++) {
        pthread_join(threads[i], NULL);
    }

    return 0;
}


/*

Output2:

gcc Stage2_ListofNumbersAndThreads.c -o 2.out -pthread
./2.out 5 10 15

Thread 0: 5
Thread 0: 4
Thread 0: 3
Thread 0: 2
Thread 0: 1
Thread 0: 0
Thread 1: 10
Thread 1: 9
Thread 1: 8
Thread 1: 7
Thread 1: 6
Thread 1: 5
Thread 1: 4
Thread 1: 3
Thread 1: 2
Thread 1: 1
Thread 1: 0
Thread 2: 15
Thread 2: 14
Thread 2: 13
Thread 2: 12
Thread 2: 11
Thread 2: 10
Thread 2: 9
Thread 2: 8
Thread 2: 7
Thread 2: 6
Thread 2: 5
Thread 2: 4
Thread 2: 3
Thread 2: 2
Thread 2: 1
Thread 2: 0

*/