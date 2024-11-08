#ifndef SUPERVISOR_SUPERVISOR_H_
#define SUPERVISOR_SUPERVISOR_H_

# define IMU_DRIVER_DIRECTORY "./imu_driver"
# define PERIOD_MS 500
# define SLEEP_MS 100

int GetPidByName(const char *process_name);
void DriverHandler(int num);
void EnsureDriverData();

#endif  // SUPERVISOR_SUPERVISOR_H_