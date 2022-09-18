#include "GhostEyes.h"

GhostEyes::GhostEyes(int x, int y, int width, int height, ofImage spriteSheet): Entity(x, y, width, height)
{
    sprite.cropFrom(spriteSheet, 64, 112, 16, 16);
}

void GhostEyes::setCoords(vector<vector<int>> coords) {this->ghostCoords = coords;};

void GhostEyes::tick(){
    
    if(!ghostCoords.empty()){
        int nextX = ghostCoords[0][0];
        int nextY = ghostCoords[0][1];

        if(nextX > x) x+=speed; // Next move is right
        if(nextX < x) x-=speed; // Next move is left
        if(nextY > y) y+=speed; // Next move is up
        if(nextY < y) y-=speed; // Next move is down
        ghostCoords.erase(ghostCoords.begin());
    }
    else
        atSpawn = true;
}

bool GhostEyes::getRemove() { return atSpawn;}