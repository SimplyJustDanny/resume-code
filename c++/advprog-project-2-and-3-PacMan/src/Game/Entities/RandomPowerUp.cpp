#include "RandomPowerUp.h"

void RandomPowerUp::activate(Player *player){
    randomScore = ofRandom(0, 800);
    player->setScore(player->getScore() + randomScore);
};