#include "supervisor.h"

#include <signal.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

// Flag to help comunicate timer handler with main function
int flag_make_driver = 0;

/**
 * @brief Gets the PID of a running process with the same given name.
 *
 * Given a process name, the function executes a command and extracts the
 * PID that it produces, specifically of a running process with the same name.
 * Should no PID be produced, the value defaults to -1.
 *
 * @param[in] process_name A name to be associated with a running process.
 *
 * @return PID of the inputted name, as an int.
 *
 * @note Meant to be run inside DriverHandler(), a timer-based signal handler.
 *
 * @example
 * GetPidByName(imu_driver);
 * If a running process named imu_driver exists, it returns its PID
 * Otherwise, returns -1
 */
int GetPidByName(const char *process_name) {
  // Parse input onto a command
  int pid;
  char command[256];
  snprintf(command, sizeof(command), "pgrep -x %s", process_name);

  // Tries to run the command to get an output
  FILE *fp = popen(command, "r");
  if (fp == NULL) {
    perror("popen");
    return -1;
  }

  // Output has to be the PID if it exists, default value is -1 if it fails
  pid = -1;
  if (fscanf(fp, "%d", &pid) == 1) {
    // Successfully retrieved a PID
  }

  // Close file and return
  pclose(fp);
  return pid;
}

/**
 * @brief Raises flag_make_driver as a sigaction handler.
 *
 * Increments flag_make_driver, with the purpose of this function
 * being used as a timer-based sigaction handler with 1.5s interval
 * Said flag allows EnsureDriverData() to boot an instance of
 * the program imu_driver.
 *
 * @param[in] num What kind of signal was received.
 *
 * @note This is a handler meant for EnsureDriverData().
 *
 * @example
 * DriverHandler(0);
 * // flag_make_driver is now 1
 */
void DriverHandler(int num) {
  char buf[64];
  int driver_pid;

  // Try to extract PID from a potentially running process of imu_driver
  driver_pid = GetPidByName("imu_driver");

  // Print it onto terminal through the buffer
  snprintf(buf, sizeof(buf), "%d\n", driver_pid);
  write(1, buf, strlen(buf));

  // If PID is -1, raise a flag to boot a new imu_driver instance
  if (driver_pid < 0) {
    flag_make_driver++;
  }
}

/**
 * @brief Checks if imu_driver is running and boots an instance itself if not.
 *
 * Sets up and initializes a timer with a 1.5s interval that checks on whether
 * or not a process named imu_driver is running. If it's not, fork and exec
 * said process from the execution directory.
 *
 * @note Requires imu_driver to be in the same directory this program runs from.
 *
 * @example
 * EnsureDriverData()
 * // Checks if imu_driver exists and continually prints its PID
 * // Otherwise, forks and execs its own instance of imu_driver if
 * // The process is in the same directory
 */
void EnsureDriverData() {
  // Initialize PID, file pointer and time-based variables
  pid_t id;
  FILE *fptr;
  timer_t timer_id;
  struct sigaction timer_action;
  struct sigevent timer_event;
  struct itimerspec timer_params;
  int signum = SIGRTMIN;

  // Configure sigaction settings to enable timer
  // Also having the sigaction triggered by SIGRTMIN
  timer_action.sa_handler = DriverHandler;
  timer_action.sa_flags = 0;
  sigaction(SIGRTMIN, &timer_action, NULL);
  timer_event.sigev_notify = SIGEV_SIGNAL;
  timer_event.sigev_signo = signum;

  // Configure timer settings to run a periodic 1.5s
  // Timer triggers SIGRTMIN instead to prevent conflict with imu_driver timer
  timer_create(CLOCK_REALTIME, &timer_event, &timer_id);
  timer_params.it_value.tv_sec = 1;
  timer_params.it_value.tv_nsec = PERIOD_MS * 1000000;
  timer_params.it_interval.tv_sec = 1;
  timer_params.it_interval.tv_nsec = PERIOD_MS * 1000000;

  // Start timer
  timer_settime(timer_id, 0, &timer_params, NULL);

  // Main function's infinite loop until program is terminated manually
  while ("True") {
    // Waits until program detects that imu_driver isn't running
    if (flag_make_driver) {
      // Create a fork and have the child run imu_driver from this directory
      // NOTE: Make sure that imu_driver is in the directory you run this from
      id = fork();
      if (id == 0) {
        execlp(IMU_DRIVER_DIRECTORY, IMU_DRIVER_DIRECTORY, NULL);
      }

      // Lower flag to prevent code from running twice
      flag_make_driver = 0;
    }
    // Sleeps for 100ms while looping to reduce CPU consumption
    usleep(SLEEP_MS * 1000);
  }
}