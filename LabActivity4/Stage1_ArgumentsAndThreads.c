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
        pthread_join(threads[i], NULL)
    }

    return 0;
}