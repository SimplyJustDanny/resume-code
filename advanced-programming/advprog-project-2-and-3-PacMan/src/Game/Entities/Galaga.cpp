#include "Galaga.h"

Galaga::Galaga(int x, int y, int width, int height, ofImage spriteSheet): Entity(x, y, width, height){
    sprite.cropFrom(spriteSheet, 80, 32, 16, 16);
}