#pragma once

#include "Powerup.h"

class StrawberryPowerup : public Powerup {
    private:
        int rank = 3;
    public:
        virtual void activate(Player* player);
        int getRank(){return this->rank;};
};