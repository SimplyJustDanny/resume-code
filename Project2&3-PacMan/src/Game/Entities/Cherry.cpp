#include "Cherry.h"

Cherry::Cherry(int x, int y, int width, int height, ofImage spriteSheet): Entity(x, y, width, height){
    sprite.cropFrom(spriteSheet, 0, 32, 16, 16);
}