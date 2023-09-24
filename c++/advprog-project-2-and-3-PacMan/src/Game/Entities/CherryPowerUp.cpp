#include "CherryPowerUp.h"

void CherryPowerUp::activate(Player *player){
    ogEntities = player->getOriginalEntities();
    int randomIndex = ofRandom(0, ogEntities.size());
    int newX = ogEntities[randomIndex]->getBounds().getX();
    int newY = ogEntities[randomIndex]->getBounds().getY();
    player->setX(newX);
    player->setY(newY);
};