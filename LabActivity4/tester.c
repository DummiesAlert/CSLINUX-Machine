//Question 2:

#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

void *printer (void *arg) {

    int *data = (int *)arg;
    int thread_id = data[0];
    int start_num = data[1];


    for (int i = start_num; i >= 0; i--) {
        printf("Thread %d: %d\n", thread_id, i);
    }

    return NULL;
}

int main (int argc, char *argv[]) {

    int num = argc - 1;
    pthread_t threads[num];


    int thread_data[num][2];

    for (long i = 0; i < num; i++) {
        int val = atoi(argv[i + 1]);

        if (val >= 100) {
            printf("Error: Number %d is not less than 100\n", val);
            return 1;
        }

        thread_data[i][0] = i + 1;
        thread_data[i][1] = val;


        pthread_create(&threads[i], NULL, printer, (void *)thread_data[i]);
    }

    for (long i = 0; i < num; i++) {
        pthread_join(threads[i], NULL);
    }

    return 0;
}

