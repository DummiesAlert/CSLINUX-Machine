// Write a C program which takes a number n for its argument. It then creates n "Racers", each with their own thread and ID. Each racer will print
    // their ID and then should loop, incrementing a global counter. The race ends when one racer increments the global counter. The race ends when
    // one racer increments the global counter over 1,000,000. Print the racer which won and the value of the counter

#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

long globalCounter = 0;
int winnerID = -1;
long winningRacer = 0;
pthread_mutex_t lock;

void *racer(void *arg) {
    long id = (long)arg;
    printf("Racer %ld has joined the race!\n", id);

    while (1) {
        pthread_mutex_lock(&lock);

        if (globalCounter >= 1000000) {
            pthread_mutex_unlock(&lock);
            break;
        }

        globalCounter++;

        if (globalCounter >= 1000000 && winnerID == -1) {
            winnerID = (int)id;
            winningRacer = globalCounter;
        }

        pthread_mutex_unlock(&lock);
    }

    return NULL;
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Error: Please provide the number of racers.\n");
        return 1;
    }

    int validRacer = atoi(argv[1]);
    if (validRacer <= 0) {
        printf("Error: Please provide a valid positive integer.\n");
        return 1;
    }

    pthread_t threads[validRacer];
    pthread_mutex_init(&lock, NULL);

    printf(\n);

    for (long i = 0; i < validRacer; i++) {
        pthread_create(&threads[i], NULL, racer, (void *)(i + 1));
    }

    for (int i = 0; i < validRacer; i++) {
        pthread_join(threads[i], NULL);
    }

    printf("\n--- Race Results ---\n");
    printf("Winner: Racer %d\n", winnerID);
    printf("Global Counter: %ld\n", winningRacer);

    pthread_mutex_destroy(&lock);

    return 0;
}

/*

Output4:

gcc Stage4_NumbersAndThreads.c -o 4.out
./4.out 5

Racer 2 has joined the race!
Racer 3 has joined the race!
Racer 1 has joined the race!
Racer 4 has joined the race!
Racer 5 has joined the race!

--- Race Results ---
Winner: Racer 5
Global Counter: 1000000

*/