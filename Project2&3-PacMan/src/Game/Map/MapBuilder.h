#pragma once

#include "ofMain.h" 
#include "Map.h"
#include "Dot.h"
#include "BigDot.h"
#include "Ghost.h"
#include "Cherry.h"
#include "Strawberry.h"
#include "Apple.h"
#include "Orange.h"

class MapBuilder {
    public:
        MapBuilder();
	    Map* createMap(ofImage, int);

	private:
        vector<ofImage> bound;
        int pixelMultiplier;
        ofColor boundBoundBlock;
        ofColor pacman;
        ofColor ghostC;
	    ofColor dotC;
	    ofColor bigDotC;
        ofColor cherryC;
        ofColor strawberryC;
        ofColor randomSpriteC;
        ofImage pacmanSpriteSheet;
        ofImage tempBound;
        ofImage getSprite(ofImage, int, int);
        EntityManager* entityManager;
        vector<Entity*> entities;
        int randomIndex;
        int newX;
        int newY;
        int randomNum;
        int playerSelected;
};