#pragma once

#include "Powerup.h"

class UltimatePowerup : public Powerup {
    private:
        int rank = 4;
    public:
        virtual void activate(Player* player);
        int getRank(){return this->rank;};
};