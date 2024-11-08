#ifndef IMUDRIVER_TIMER_H_
#define IMUDRIVER_TIMER_H_

#define IMU_DATA_DIRECTORY "./imu_data.txt"
#define PERIOD_MS 200

typedef struct {
  double time;
  double p_x;
  double p_y;
  double v_x;
  double v_y;
  double acc_x;
  double acc_y;
} RobotState;

void TimerHandler(int num);
void GenerateDriverData(RobotState robot_state);

#endif  // IMUDRIVER_TIMER_H_