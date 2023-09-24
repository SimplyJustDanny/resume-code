#include "Apple.h"

Apple::Apple(int x, int y, int width, int height, ofImage spriteSheet): Entity(x, y, width, height){
    sprite.cropFrom(spriteSheet,48,32,16,16);
}