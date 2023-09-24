#pragma once

#include "Powerup.h"

class RandomPowerUp : public Powerup {
    private:
        int randomScore;
        int rank = 0;
    public:
        virtual void activate(Player* player);
        int getRank(){return this->rank;};
};