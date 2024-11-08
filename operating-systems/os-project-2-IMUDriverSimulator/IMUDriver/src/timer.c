#include "timer.h"

#include <signal.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <time.h>
#include <unistd.h>

// Flag to help comunicate timer handler with main function
int flag_generate_data = 0;

/**
 * @brief Raises flag_generate_data as a sigaction handler.
 *
 * Increments flag_generate_data, with the purpose of this function
 * being used as a timer-based sigaction handler with a 200ms interval
 * Said flag used to notify GenerateDriverData() that it can calculate
 * the next state of the robot driver and append it to its file.
 *
 * @param[in] num What kind of signal was received.
 *
 * @note This is a handler meant for GenerateDriverData().
 *
 * @example
 * TimerHandler(0);
 * // flag_generate_data is now 1
 */
void TimerHandler(int num) { flag_generate_data++; }

/**
 * @brief Generates data for the simulated robot driver in text file.
 *
 * Either creates a file called imu_data.txt or extracts data from it
 * onto the robot_state input. Afterwards, a 200ms timer starts and
 * begins making calculations that are appended onto imu_data.txt.
 * This program goes on forever until terminated manually.
 *
 * @param[in] robot_state Where data such as time and position are stored.
 *
 * @note Meant to be used in conjunction with supervisor program.
 *
 * @example
 * RobotState robot_state = {
 *   .time = 0,
 *   .p_x = 20,
 *   .p_y = 10,
 *   .v_x = 0,
 *   .v_y = 0,
 *   .acc_x = 0.15,
 *   .acc_y = 0.06,
 * };
 * GenerateDriverData(robot_state);
 * // imu_data.txt is either created or robot_state is updated to
 * // match imu_data.txt, promptly before going into an infinite loop
 * // that perpetually appends imu_data.txt
 */
void GenerateDriverData(RobotState robot_state) {
  // Lots of variables to declare here
  // Starting off with file pointers and time-based variables
  FILE* fptr;
  timer_t timer_id;
  struct timespec start;
  struct timespec end;
  struct sigaction timer_action;
  struct itimerspec timer_params;
  double elapsed;
  // Extract struct member pointers for fast reference
  double* time = &robot_state.time;
  double* acc_x = &robot_state.acc_x;
  double* acc_y = &robot_state.acc_y;
  double* vel_x = &robot_state.v_x;
  double* vel_y = &robot_state.v_y;
  double* pos_x = &robot_state.p_x;
  double* pos_y = &robot_state.p_y;
  // Make array of pointers and a few char pointers for tokenization
  double* params[] = {time, pos_x, pos_y, vel_x, vel_y, acc_x, acc_y};
  int param_cnt = 0;
  char buf[128];
  char str[128];
  char* token;

  // Configure sigaction settings to enable timer
  timer_action.sa_handler = TimerHandler;
  timer_action.sa_flags = 0;
  sigaction(SIGALRM, &timer_action, NULL);

  // Configure timer settings to run a periodic 200ms
  timer_create(CLOCK_REALTIME, NULL, &timer_id);
  timer_params.it_value.tv_sec = 0;
  timer_params.it_value.tv_nsec = PERIOD_MS * 1000000;
  timer_params.it_interval.tv_sec = 0;
  timer_params.it_interval.tv_nsec = PERIOD_MS * 1000000;

  // If file exists, then open it and extract its last line
  if (access(IMU_DATA_DIRECTORY, F_OK) == 0) {
    fptr = fopen(IMU_DATA_DIRECTORY, "r");
    while (fgets(buf, sizeof(buf), fptr)) {
      // If the buffer only has terminating character, then str has last line
      if (strlen(buf) > 1) {
        strcpy(str, buf);
      }
    }
    fclose(fptr);
    // Tokenize extracted string, cast to doubles, and store in params by array
    token = strtok(str, " ,\n");
    while (token != NULL) {
      sscanf(token, "%lf", params[param_cnt++]);
      token = strtok(NULL, " ,\n");
    }
  } else {
    // Else, open file in append and write initial state
    fptr = fopen(IMU_DATA_DIRECTORY, "a");
    fprintf(fptr, "%.2lf, %.4lf, %.4lf, %.4lf, %.4lf, %.4lf, %.4lf\n", *time,
            *pos_x, *pos_y, *vel_x, *vel_y, *acc_x, *acc_y);
    fclose(fptr);
  }

  // After handling file, start timer and time measurer
  timer_settime(timer_id, 0, &timer_params, NULL);
  clock_gettime(CLOCK_REALTIME, &start);

  // Continually calculates the next step of the process until terminated
  while ("True") {
    // Waits until timer raises flag to append file
    if (flag_generate_data) {
      // Increment time and use standard physics equations
      *time += 0.2;
      *vel_x += *acc_x * 0.2;
      *vel_y += *acc_y * 0.2;
      *pos_x += *vel_x * 0.2;
      *pos_y += *vel_y * 0.2;

      // Immediately open, append, and close file to save written data
      fptr = fopen(IMU_DATA_DIRECTORY, "a");
      fprintf(fptr, "%.2lf, %.4lf, %.4lf, %.4lf, %.4lf, %.4lf, %.4lf\n", *time,
              *pos_x, *pos_y, *vel_x, *vel_y, *acc_x, *acc_y);
      fclose(fptr);

      // Get the measured time for the calculations to ensure it's roughly 200ms
      // Lower flag to prevent code from running twice and reset time measure
      clock_gettime(CLOCK_REALTIME, &end);
      elapsed =
          (end.tv_sec - start.tv_sec) + (end.tv_nsec - start.tv_nsec) / 1E9;
      printf("Line appended in %.3lf seconds.\n", elapsed);
      flag_generate_data = 0;
      clock_gettime(CLOCK_REALTIME, &start);
    }
  }
}