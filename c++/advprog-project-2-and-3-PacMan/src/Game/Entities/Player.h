#pragma once

#include "Animation.h"
#include "EntityManager.h"
#include "SelectState.h"

enum MOVING {
	MUP,
	MDOWN,
	MLEFT,
	MRIGHT,
};

class Powerup;

class Player: public Entity{

    private:
        int spawnX, spawnY;
        unsigned int health=3;
        int score=0;
        bool canMoveUp, canMoveDown, canMoveRight, canMoveLeft;
        int speed = 4;
        int timer = 0;
        bool walking = false;
        bool evade = false;
        bool galagaSpawn = false;
        MOVING moving;
        FACING facing = DOWN;
        ofImage up, down, left, right;
        Animation *walkUp;
        Animation *walkDown;
        Animation *walkLeft;
        Animation *walkRight;
        EntityManager* em;
        vector<Entity*> originalEntities;
        vector<Powerup*> powerupsCollected;
        int playerSelected = 0;
        string playerDisplay = "Pac-Man";
        string powerupList = "";
        ofImage ghostEyesImg;
        bool isNewGhost; // For checking if eyes are at spawn (ghost should respawn)
        bool activeGPS = false;
        int distX = 9999;
        int distY = 9999;
        int maze;
    public:
        Player(int, int, int , int, EntityManager*, int);
        ~Player();
        int getHealth();
        int getScore();
        int getSpeed();
        int getPowerup();
        FACING getFacing();
        vector<Powerup*> getPowerupsCollected();
        void setHealth(int);
        void setScore(int);
        void setFacing(FACING facing);
        void setSpeed(int);
        void setPowerup(int);
        void setEvade(bool);
        void setPowerupsCollected(vector<Powerup*> h);
        void tick();
        void render();
        void keyPressed(int);
        void keyReleased(int);
        void damage(Entity* damageSource);
        void mousePressed(int, int, int);
        void reset();
        void checkCollisions();
        void die();
        int getDotSize();
        vector<Entity*> getOriginalEntities();
        void setX(int newX);
        void setY(int newY);
        void setNewGhost(bool);
        bool getNewGhost();
        void findPowerup(int, int, int, int, int, string);
};