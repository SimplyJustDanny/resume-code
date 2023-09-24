#pragma once

#include "State.h"
#include "Button.h"
#include "Animation.h" 

class SelectState : public State {
private:
	ofImage img1;
	Button *pacmanButton;
	Button *msPacmanButton;
	Button *jrPacmanButton;
	Button *pacmaniaButton;
	Button *backButton;
	Animation* anim;
	int playerSelected;
public:
	SelectState();
	~SelectState();
	void tick();
	void render();
	void keyPressed(int key);
	void mousePressed(int x, int y, int button);
	void reset();
	void setSprite(int player);
	int getSprite();
};
