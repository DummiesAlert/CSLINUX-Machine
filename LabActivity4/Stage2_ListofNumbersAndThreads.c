// Write a C program which takes list of numbers (all less than 100) for its argument. Then it starts as many threads as there are numbers and in each
    // thread it counts down from the number given to 0, then ends. 

#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>

typedef struct {
    int threadNumber;
    int numbers;
}

ThreadNumbers;

void *countdown(void *arg) {
    ThreadNumbers * number = (ThreadNumbers *)arg;

    for (int i = number->numbers; i >= 0; i--) {
        printf("Thread %d: %d\n", ThreadNumbers->threadNumber, i);
    }

    return NULL;
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Invalid or No Arguments are provided\n", argv[0]);
        return 1;
    }

    int count = argc - 1;

    pthread_t threads[count];
    ThreadNumbers numbers[count];

    for (int i = 0; i < count; i++) {
        numbers[i].threadNumber = i;
        numbers[i].numbers = atoi(argv[i + 1]);

        if (numbers[i].numbers < 0 || numbers[i].numbers > 100) { 
            printf("Number is not less than 100!!!! \nNumber: %d\n", numbers[i]); 
            return 1;
        }

        pthread_create(&threads[i], NULL, countdown, &numbers[i]);
        
        pthread_join(threads[i], NULL);
    }
    return 0;
}

/*

Output: 

gcc Stage2_ListofNumbersAndThreads.c -o 2.out -pthread
./2.out 

*/