// Write a C program which takes a number n for its argument. It then creates n "Racers", each with their own thread and ID. Each racer will print
    // their ID and then should loop, incrementing a global counter. The race ends when one racer increments the global counter. The race ends when
    // one racer increments the global counter over 1,000,000. Print the racer which won and the value of the counter 

#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

#define LIMIT 1000000

int counter = 0;
int winner = -1;

pthread_mutex_t lock;

typedef struct {
    int id;
} Racer;

void *race(void *arg) {
    Racer *racer = (Racer *)arg;

    printf("Racer %d started\n", racer->id);

    while (1) {

        pthread_mutex_lock(&lock);

        // Stop if race already finished
        if (counter > LIMIT) {
            pthread_mutex_unlock(&lock);
            break;
        }

        counter++;

        // Check for winner
        if (counter > LIMIT) {
            winner = racer->id;

            printf("\nRacer %d wins!\n", winner);
            printf("Final counter value: %d\n", counter);

            pthread_mutex_unlock(&lock);
            break;
        }

        pthread_mutex_unlock(&lock);
    }

    return NULL;
}

int main(int argc, char *argv[]) {

    if (argc != 2) {
        printf("Usage: %s number_of_racers\n", argv[0]);
        return 1;
    }

    int n = atoi(argv[1]);

    if (n <= 0) {
        printf("Number of racers must be positive\n");
        return 1;
    }

    pthread_t threads[n];
    Racer racers[n];

    pthread_mutex_init(&lock, NULL);

    // Create racers
    for (int i = 0; i < n; i++) {
        racers[i].id = i;

        pthread_create(&threads[i], NULL, race, &racers[i]);
    }

    // Wait for racers to finish
    for (int i = 0; i < n; i++) {
        pthread_join(threads[i], NULL);
    }

    pthread_mutex_destroy(&lock);

    return 0;
}