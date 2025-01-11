#ifndef MOUSESAVER_SAVER_H_
#define MOUSESAVER_SAVER_H_

#define BUFFER_DEVICE_DIR "/dev/fb0"
#define MOUSE_DEVICE_DIR "/dev/input/mice"
#define BINARY_DIR "./mouse_data.dat"

void SaveMouseData();

#endif  // MOUSESAVER_SAVER_H_