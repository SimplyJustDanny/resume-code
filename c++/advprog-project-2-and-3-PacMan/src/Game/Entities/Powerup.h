#pragma once

#include "Player.h"

class Powerup{
    private:
        int rank = 0;
    public:
        virtual void activate(Player* player) = 0;
        virtual int getRank(){return this->rank;};
        virtual int compareTo(Powerup* p2){ return this->getRank() - p2->getRank(); }
};