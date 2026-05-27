#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

long global_counter = 0;
int winner_id = -1;
long winning_value = 0;
pthread_mutex_t lock;

void *racer(void *arg) {
    long id = (long)arg;
    printf("Racer %ld has joined the race!\n", id);

    while (1) {
        pthread_mutex_lock(&lock);

        if (global_counter >= 1000000) {
            pthread_mutex_unlock(&lock);
            break;
        }

        global_counter++;

        if (global_counter >= 1000000 && winner_id == -1) {
            winner_id = (int)id;
            winning_value = global_counter;
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

    int n = atoi(argv[1]);
    if (n <= 0) {
        printf("Error: Please provide a valid positive integer.\n");
        return 1;
    }

    pthread_t threads[n];
    pthread_mutex_init(&lock, NULL);


    for (long i = 0; i < n; i++) {

        pthread_create(&threads[i], NULL, racer, (void *)(i + 1));
    }

    for (int i = 0; i < n; i++) {
        pthread_join(threads[i], NULL);
    }

    printf("\n--- Race Results ---\n");
    printf("Winner: Racer %d\n", winner_id);
    printf("Final Counter Value: %ld\n", winning_value);

    pthread_mutex_destroy(&lock);

    return 0;
}
