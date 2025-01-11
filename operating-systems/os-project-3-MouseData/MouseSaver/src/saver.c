#include "saver.h"

#include <fcntl.h>
#include <linux/fb.h>
#include <linux/input.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int no_signal = 1;

/**
 * @brief Lowers a flag when receiving a SIGINT
 *
 * Upon receiving a SIGINT, this handler function lowers the
 * global flag no_signal that ceases loops for some functions.
 *
 * @param[in] num Signal sent
 *
 * @note Meant to be used as a handler for SaveMouseData()
 *
 * @example
 * SignalHandler(1);
 * // no_signal is set to 0
 */

void SignalHandler(int num) { no_signal = 0; }

/**
 * @brief Records mouse movements on display onto a binary file
 *
 * This is a more in-depth description of the function, which may
 * add details not originally present in the brief
 *
 * @note Has a signal handler for SIGINT to stop and close the files
 *
 * @example
 * SaveMouseData()
 * // Prints a bunch of data regarding your mouse cursor
 * // In the terminal directory, a "mouse_data.dat" file can be found
 */

void SaveMouseData() {
  // Initiate screen and mouse variables
  int buffer_fd;
  int x_res;
  int y_res;
  struct fb_var_screeninfo vinfo;
  int mouse_fd;
  int cursor_x;
  int cursor_y;
  int cursor_dx;
  int cursor_dy;
  float terminal_x;
  float terminal_y;
  signed char mouse_data[3];
  unsigned int terminal_coords[2];
  FILE* fptr;
  struct sigaction sigact;

  // Set up signal handling for SIGINT
  sigact.sa_handler = SignalHandler;
  sigaction(SIGINT, &sigact, NULL);

  // Extract screen resolution via frame buffer
  buffer_fd = open(BUFFER_DEVICE_DIR, O_RDONLY);
  if (buffer_fd == -1) {
    perror("Error opening buffer device");
    exit(1);
  }
  if (ioctl(buffer_fd, FBIOGET_VSCREENINFO, &vinfo) == -1) {
    perror("Error reading variable information");
    exit(3);
  }
  x_res = vinfo.xres;
  y_res = vinfo.yres;
  close(buffer_fd);

  // Read mouse inputs from Linux's generic device files
  mouse_fd = open(MOUSE_DEVICE_DIR, O_RDONLY);
  if (mouse_fd == -1) {
    perror("Error opening mouse device");
    exit(1);
  }

  // Initiate mouse coords, then open binary file and raise loop flag
  // Note that the sigaction has padding which is accordingly subtracted
  cursor_x = (int)((x_res / 2) - 128);
  cursor_y = (int)((y_res / 2) - 16);
  terminal_coords[0] = (unsigned int)(100 * cursor_x / (x_res - 256));
  terminal_coords[1] = (unsigned int)(25 * cursor_y / (y_res - 256));
  fptr = fopen(BINARY_DIR, "wb");
  if (fptr == NULL) {
    printf("Error opening or creating binary file.");
    exit(1);
  }

  // Loop perpetually to read mouse coords, until signal is sent
  printf("Listening for mouse movement. Move the mouse.\n");
  while (no_signal) {
    if (read(mouse_fd, mouse_data, sizeof(mouse_data)) > 0) {
      cursor_dx = mouse_data[1];
      cursor_dy = mouse_data[2];
      cursor_x += cursor_dx;
      cursor_y -= cursor_dy;
      terminal_x = 100 * (float)cursor_x / (float)(x_res - 256);
      terminal_y = 25 * (float)cursor_y / (float)(y_res - 32);
      terminal_coords[0] = (unsigned int)terminal_x;
      terminal_coords[1] = (unsigned int)terminal_y;

      printf(
          "Screen x: %d, Screen y: %d, dx: %d, dy: %d, Terminal x: %4f, "
          "Terminal y: %4f\n",
          cursor_x, cursor_y, cursor_dx, cursor_dy, terminal_x, terminal_y);
    }
    fwrite(&terminal_coords[0], sizeof(unsigned int), 1, fptr);
    fwrite(&terminal_coords[1], sizeof(unsigned int), 1, fptr);
  }
  // Dont't forget to close file after SIGINT
  fclose(fptr);
  close(mouse_fd);
}