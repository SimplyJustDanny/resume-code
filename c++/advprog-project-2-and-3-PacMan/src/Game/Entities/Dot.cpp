#include "Dot.h"

Dot::Dot(int x, int y, int width, int height, ofImage spriteSheet): Entity(x, y, width, height){
    sprite.cropFrom(spriteSheet, 112,16,16,16);
}