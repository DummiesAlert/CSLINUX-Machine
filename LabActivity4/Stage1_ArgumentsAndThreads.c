// Write a C program which takes a number n for its argument. Then it starts n threads, has each print a message with its numbers and ends.

#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>

void *printer(void *n) {
    printf("This is Thread %ld\n", (long)n);
    return NULL;
}

int main(int argc, char *argv[]) {

    int num = atoi(argv[1]);
    pthread_t threads[num];

    for (long i = 0; i < num; i++) {
        pthread_create(&threads[i], NULL, printer, (void *)i);
    }

    for (int i = 0; i < num; i++) {
        pthread_join(threads[i], NULL);
    }

    return 0;
}

/*

Output1:

gcc Stage1_ArgumentsAndThreads.c -o 1.out
./1.out 16

This is Thread 9
This is Thread 10
This is Thread 3
This is Thread 6
This is Thread 11
This is Thread 12
This is Thread 2
This is Thread 7
This is Thread 8
This is Thread 13
This is Thread 14
This is Thread 15
This is Thread 5
This is Thread 1
This is Thread 4
This is Thread 0
*/