#pragma once

#include "State.h"
#include "Button.h"

class WinState : public State
{
    private:
        Button *restartButton;
        Button *mainMenuButton;
        Button *quitButton;
        int finalScore;
    public:
        WinState();
	    void reset();
		void tick();
		void render();
		void keyPressed(int key);
		void mousePressed(int x, int y, int button);
        void setScore(int s);

};