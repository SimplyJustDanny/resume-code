#pragma once

#include "Powerup.h"

class SpeedPowerup : public Powerup {
    private:
        int rank = 1;
    public:
        virtual void activate(Player* player);
        int getRank(){return this->rank;};
};