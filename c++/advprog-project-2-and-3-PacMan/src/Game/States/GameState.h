#pragma once

#include "State.h"
#include "Player.h"
#include "MapBuilder.h"

class GameState: public State{
    public: 
        GameState(int);
		virtual ~GameState();
		void reset();
		void tick();
		void render();
		void keyPressed(int key);
		void mousePressed(int x, int y, int button);
		void keyReleased(int key);
		void setSprite(int spritesheet) { playerSelected = spritesheet; }
		int getFinalScore();
		int getSprite() { return playerSelected; }

		bool hasPaused(){
			return paused;
		}
		void setPaused(bool paused){
			this->paused = paused;
		}

	private:
		ofSoundPlayer music;
		ofImage mapImage;
		Map* map;
		int finalScore=0;
		bool paused;
		int playerSelected = 0;

};