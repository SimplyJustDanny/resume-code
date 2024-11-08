#include "timer.h"

int main() {
  // Initialize robot data
  RobotState robot_state = {
      .time = 0,
      .p_x = 20,
      .p_y = 10,
      .v_x = 0,
      .v_y = 0,
      .acc_x = 0.15,
      .acc_y = 0.06,
  };

  GenerateDriverData(robot_state);

  return 0;
}