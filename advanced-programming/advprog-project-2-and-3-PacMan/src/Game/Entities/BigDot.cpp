#include "BigDot.h"

BigDot::BigDot(int x, int y, int width, int height, ofImage spriteSheet): Entity(x, y, width, height){
    sprite.cropFrom(spriteSheet, 112, 0, 16, 16);
}