// Implement the Second Readers-Writers Problem: This is writer priority, readers can access the resource at the same time, but once a writer has requested 
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


pthread_mutex_t readcount_mutex;
pthread_mutex_t writecount_mutex;

pthread_mutex_t readTry;
pthread_mutex_t reader_mutex;
pthread_mutex_t writer_mutex;

int readcount = 0;
int writecount = 0;

typedef struct {
	int ID;
} thread_arg_t;

void* reader_go(void* arg) {

	thread_arg_t thread_arg = *(thread_arg_t*) arg;

	printf("Reader %d: Starting.\n", thread_arg.ID);

    // Added Here ---------------------------------------------------------------------------------------
    pthread_mutex_lock (&readTry);
    pthread_mutex_lock (&reader_mutex);
    pthread_mutex_lock (&readcount_mutex);

    readcount++;
    if (readcount == 1)
        pthread_mutex_lock (&writer_mutex);
    
    pthread_mutex_lock (&readcount_mutex);
    pthread_mutex_unlock (&reader_mutex);

    pthread_mutex_unlock (&readTry);
    // Ended Here ---------------------------------------------------------------------------------------

	for (int i = 0; i < READER_LOOP; i++) {

		int sleep_time = rand() % SLEEP_MAX;
		printf("Reader %d: Starting Reading for %d usec\n", 
				thread_arg.ID,
				sleep_time);
		usleep(sleep_time); //usleep takes time in microseconds

		printf("Reader %d: Done Reading\n", thread_arg.ID);
	}

    // Added Here ---------------------------------------------------------------------------------------
    pthread_mutex_lock (&readcount_mutex);

    readcount--;
    if (readcount == 0)
        pthread_mutex_unlock (&writer_mutex);
    
    pthread_mutex_unlock (&readcount_mutex);
    // Ended Here ---------------------------------------------------------------------------------------

	printf("Reader %d: Finished\n", thread_arg.ID);

	return NULL;

}

void* writer_go(void* arg) {

	thread_arg_t thread_arg = *(thread_arg_t*) arg;

	printf("Writer %d: Starting.\n", thread_arg.ID);

    // Added Here ---------------------------------------------------------------------------------------

    pthread_mutex_lock (&writecount_mutex);

    writecount++;
    if (writecount == 1)
        pthread_mutex_lock (&reader_mutex);

    pthread_mutex_unlock (&writecount_mutex);

    // Ended Here ---------------------------------------------------------------------------------------

	for (int i = 0; i < WRITER_LOOP; i++) {

        // Added Here ---------------------------------------------------------------------------------------
        
        pthread_mutex_lock (&writer_mutex);
        
        // Ended Here ---------------------------------------------------------------------------------------

		int sleep_time = rand() % SLEEP_MAX;
		printf("Writer %d: Starting writing for %d usec\n", 
				thread_arg.ID,
				sleep_time);
		usleep(sleep_time); //usleep takes time in microseconds

		printf("Writer %d: Done writing\n", thread_arg.ID);

        // Added Here ---------------------------------------------------------------------------------------
        
        pthread_mutex_unlock (&writer_mutex);
        
        // Ended Here ---------------------------------------------------------------------------------------
	}

    // Added Here ---------------------------------------------------------------------------------------
    
    pthread_mutex_lock (&writecount_mutex);
    
    writecount--;
    if (writecount == 0)
        pthread_mutex_unlock (&reader_mutex);
    
    pthread_mutex_unlock (&writecount_mutex);
    
    // Ended Here ---------------------------------------------------------------------------------------

	printf("Writer %d: Finished\n", thread_arg.ID);

	return NULL;

}

int main(int argc, char *agarv[]) {

	printf("Readers Writers Etc\n");

	srand(time(NULL)); // seeding randomizer

	pthread_mutex_init(&readcount_mutex, NULL);
	pthread_mutex_init(&writecount_mutex, NULL);

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

