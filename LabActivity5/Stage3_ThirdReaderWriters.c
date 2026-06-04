// Implement the Third Readers-Writers Problem: This is fairness priority, readers can access the resource at the same time, but once a wrtier has requested
    // access no other writer can be given access. Once the readers have cleared the writer can access.

#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

#include <stdlib.h>
#include <time.h>

#include <pthread.h>

#define SLEEP_MAX 1000

#define READER_COUNT 5
#define WRITER_COUNT 5

#define READER_LOOP 3
#define WRITER_LOOP 3


pthread_mutex_t readers_lock;
pthread_mutex_t writers_lock;

int reader_count = 0;

typedef struct {
	int ID;
} thread_arg_t;

void* reader_go(void* arg) {

	thread_arg_t thread_arg = *(thread_arg_t*) arg;

	printf("Reader %d: Starting.\n", thread_arg.ID);

	for (int i = 0; i < READER_LOOP; i++) {

		int sleep_time = rand() % SLEEP_MAX;
		printf("Reader %d: Starting Reading for %d usec\n", 
				thread_arg.ID,
				sleep_time);
		usleep(sleep_time); //usleep takes time in microseconds

		printf("Reader %d: Done Reading\n", thread_arg.ID);
	}

	printf("Reader %d: Finished\n", thread_arg.ID);

	return NULL;

}

void* writer_go(void* arg) {

	thread_arg_t thread_arg = *(thread_arg_t*) arg;

	printf("Writer %d: Starting.\n", thread_arg.ID);

	for (int i = 0; i < WRITER_LOOP; i++) {

		int sleep_time = rand() % SLEEP_MAX;
		printf("Writer %d: Starting writing for %d usec\n", 
				thread_arg.ID,
				sleep_time);
		usleep(sleep_time); //usleep takes time in microseconds

		printf("Writer %d: Done writing\n", thread_arg.ID);
	}

	printf("Writer %d: Finished\n", thread_arg.ID);

	return NULL;

}

int main(int argc, char *agarv[]) {

	printf("Readers Writers Etc\n");

	srand(time(NULL)); // seeding randomizer

	pthread_mutex_init(&readers_lock, NULL);
	pthread_mutex_init(&writers_lock, NULL);

	pthread_t reader_threads[READER_COUNT];
	thread_arg_t reader_args[READER_COUNT];

	for (int i = 0; i < READER_COUNT; i++) {
		int status;

		reader_args[i].ID = i;

		status = pthread_create(&reader_threads[i],
				NULL,
				reader_go,
				&reader_args[i]);

		if (status != 0) {
			fprintf (stderr, "Error creating Reader  %d\n", i);
			exit(status);
		}

	}

	pthread_t writer_threads[WRITER_COUNT];
	thread_arg_t writer_args[WRITER_COUNT];


	for (int i = 0; i < WRITER_COUNT; i++) {
		int status;

		writer_args[i].ID = i;

		status = pthread_create(&writer_threads[i],
				NULL,
				writer_go,
				&writer_args[i]);

		if (status != 0) {
			fprintf (stderr, "Error creating writer %d\n", i);
			exit(status);
		}

	}

	for (int i = 0; i < READER_COUNT; i++) {
		pthread_join(reader_threads[i], NULL);
	}


	for (int i = 0; i < WRITER_COUNT; i++) {
		pthread_join(writer_threads[i], NULL);
	}

}

