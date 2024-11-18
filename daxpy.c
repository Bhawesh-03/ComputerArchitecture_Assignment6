#include <stdio.h>
#include <pthread.h>

#define N 1000000  // Size of vectors
#define NUM_THREADS 4  // Number of threads

float x[N], y[N];
float a = 2.5;  // Scalar multiplier

typedef struct {
    int start;  // Start index for this thread
    int end;    // End index for this thread
} ThreadData;

void* daxpy_thread(void* arg) {
    ThreadData* data = (ThreadData*)arg;
    for (int i = data->start; i < data->end; i++) {
        y[i] = a * x[i] + y[i];
    }
    return NULL;
}

int main() {
    // Initialize vectors
    for (int i = 0; i < N; i++) {
        x[i] = i * 0.5;
        y[i] = i * 0.2;
    }

    pthread_t threads[NUM_THREADS];
    ThreadData thread_data[NUM_THREADS];
    int chunk_size = N / NUM_THREADS;

    // Create threads
    for (int i = 0; i < NUM_THREADS; i++) {
        thread_data[i].start = i * chunk_size;
        thread_data[i].end = (i == NUM_THREADS - 1) ? N : (i + 1) * chunk_size;
        pthread_create(&threads[i], NULL, daxpy_thread, &thread_data[i]);
    }

    // Join threads
    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_join(threads[i], NULL);
    }

    printf("DAXPY completed.\n");
    return 0;
}
