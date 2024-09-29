#include "visualizer.h"

#include <fcntl.h>
#include <semaphore.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <sys/time.h>

// Allocate at least 2002 in memory for both the writer and the computer
#define SHM_SIZE 2048 * sizeof(double)

#define SEM_GENERATOR "/generator"
#define SEM_ANALYZER "/analyzer"
#define SEM_VISUALIZER "/visualizer"

/**
 * @brief Plots the data from sine analysis.
 *
 * This function plots 1001 values of the sine function
 * to help visualize each value
 *
 * @note Requires SineGenerator and SineAnalyzer to run.
 */
void Visualize() {
  // TimeVal structs to calculate execution time
  struct timeval tp1;
  struct timeval tp2;
  gettimeofday(&tp1, NULL);

  // Establish variables
  key_t key;
  int shmid;
  double *data;

  // Generate key for shared memory
  key = ftok("/tmp", 65);
  if (key == -1) {
    perror("Error: FTok failure.");
    exit(EXIT_FAILURE);
  }

  // Produce semaphores
  sem_t *semaphore_generator = sem_open(SEM_GENERATOR, O_CREAT, 0666, 0);
  if (semaphore_generator == SEM_FAILED) {
    perror("Error: Generator semaphore failure.");
    exit(EXIT_FAILURE);
  }
  sem_t *semaphore_analyzer = sem_open(SEM_ANALYZER, O_CREAT, 0666, 0);
  if (semaphore_analyzer == SEM_FAILED) {
    perror("Error: Analyzer semaphore failure.");
    exit(EXIT_FAILURE);
  }
  sem_t *semaphore_visualizer = sem_open(SEM_VISUALIZER, O_CREAT, 0666, 1);
  if (semaphore_visualizer == SEM_FAILED) {
    perror("Error: Visualizer semaphore failure.");
    exit(EXIT_FAILURE);
  }

  // Allocate shared memory
  shmid = shmget(key, SHM_SIZE, 0666 | IPC_CREAT);
  if (shmid == -1) {
    perror("Error: ShMGet failure.");
    exit(EXIT_FAILURE);
  }

  // Get data pointer
  data = (double *)shmat(shmid, NULL, 0);
  if (data == (double *)-1) {
    perror("Error: ShMAt failure.");
    exit(EXIT_FAILURE);
  }

  // Visualizer doubles and sine values
  for (int i = 0; i < 1001; i++) {
    sem_wait(semaphore_analyzer);
    printf("sin(%.2lf) == %lf\n", data[0], data[1024]);
    sem_post(semaphore_visualizer);
  }
  printf("Visualizing done!\n");

  // Close semaphores then detach and clear shared memory
  sem_close(semaphore_generator);
  sem_close(semaphore_analyzer);
  sem_close(semaphore_visualizer);
  shmdt(data);
  shmctl(shmid, IPC_RMID, NULL);

  // Final results expressed in seconds
  gettimeofday(&tp2, NULL);
  double time = (tp2.tv_usec - tp1.tv_usec);
  printf("Total time of execution: %.4lf nanoseconds\n ", time);
}