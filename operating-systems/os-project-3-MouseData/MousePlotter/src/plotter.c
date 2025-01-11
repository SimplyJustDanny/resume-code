#include "plotter.h"

#include <curses.h>  // includes <stdio.h>
#include <time.h>
#include <unistd.h>

/**
 * @brief Reads binary file of coordinates and displays them in ncurse
 *
 * Creates an ncurse screen which traces a path with an asterisk.
 * The path is traced by using a symbolically linked binary file
 * that containts pairs of x and y coordinates from a resulting
 * mouse cursor path.
 *
 * @note Meant to be used with the mouse_saver program
 *
 * @example
 * SimulatePath()
 * // Should the binary file exist, an asterisk pops up and zips around
 */
void SimulatePath() {
  FILE* fptr;
  int x_read;
  int y_read;

  fptr = fopen(BINARY_LINK_DIR, "rb");

  // Initiate screen and go through
  initscr();
  while (!feof(fptr)) {
    fread(&x_read, sizeof(int), 1, fptr);
    fread(&y_read, sizeof(int), 1, fptr);
    clear();
    mvprintw(y_read, x_read, "*");
    refresh();
    usleep(10000);
  }

  fclose(fptr);

  endwin();
}