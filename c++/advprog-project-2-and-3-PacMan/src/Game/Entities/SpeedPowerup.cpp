#include "SpeedPowerup.h"

void SpeedPowerup::activate(Player *player){
    if (player->getSpeed() == 4){
        player->setSpeed(player->getSpeed()*2);
    }
    else{
        player->setSpeed(player->getSpeed()/2);   
    }
};