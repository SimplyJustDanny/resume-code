#include "GhostSpawner.h"
#include "Ghost.h"

GhostSpawner::GhostSpawner(int x, int y, int width, int height, EntityManager* em, ofImage sprite) : Entity(x, y, width, height){
    this->em = em;
    this->sprite = sprite;
    spawnGhost("red");
    spawnGhost("pink");
    spawnGhost("cyan");
    spawnGhost("orange");

}

void GhostSpawner::tick(){
    std::vector<string> colors;
    colors.push_back("red");
    colors.push_back("pink");
    colors.push_back("cyan");
    colors.push_back("orange");

    if(!ghostsSpawned || isNewGhost){
        if(spawnCounter == 0 || isNewGhost){
            spawnGhost(colors[ofRandom(4)]);
            spawnCounter = 30*5;
            isNewGhost = false;
        }else{
            spawnCounter--;
        }
    }

    if (!ghostsSpawned && em->ghosts.size() == 4){
        ghostsSpawned = true;
    }
}
void GhostSpawner::spawnGhost(string color){
    Ghost* g = new Ghost(x,y,width,height,sprite,em, color);
    em->ghosts.push_back(g);
}

void GhostSpawner::keyPressed(int key){
    std::vector<string> colors;
    colors.push_back("red");
    colors.push_back("pink");
    colors.push_back("cyan");
    colors.push_back("orange");
    if(key == 'g'){
        spawnGhost(colors[ofRandom(4)]);
    }
}

void GhostSpawner::setNewGhost(bool isNewGhost) { this->isNewGhost = isNewGhost; }