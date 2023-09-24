#pragma once

#include "Powerup.h"

class CherryPowerUp : public Powerup {
    private:
        vector<Entity*> ogEntities;
        int rank = 2;
    public:
        virtual void activate(Player* player);
        int getRank(){return this->rank;};
};