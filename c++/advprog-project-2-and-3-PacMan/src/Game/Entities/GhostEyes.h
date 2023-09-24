#pragma once

#include "Entity.h"

class GhostEyes: public Entity{
        vector<vector<int>> ghostCoords{};
        int speed = 4;
        bool atSpawn = false;
    public:
        GhostEyes(int, int, int, int, ofImage);
        void setCoords(vector<vector<int>>);
        void tick();
        bool getRemove();
};

