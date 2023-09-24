#include "SelectState.h"
#include "MenuState.h"
#include "Player.h"

SelectState::SelectState() {
    pacmanButton = new Button(ofGetWidth()/2-32, ofGetHeight()/2, 64, 50, "Pac-Man");
    msPacmanButton = new Button(ofGetWidth()/2-32, ofGetHeight()/2 + 50, 64, 50, "Ms. Pac-Man");
    jrPacmanButton = new Button(ofGetWidth()/2-32, ofGetHeight()/2 + 100, 64, 50, "Jr. Pac-Man");
    pacmaniaButton = new Button(ofGetWidth()/2-32, ofGetHeight()/2 + 150, 64, 50, "Pac-Mania");
	backButton = new Button(ofGetWidth()/2-32, ofGetHeight()/2 + 250, 64, 50, "Back");
    img1.load("images/pacman-title.png");
	vector<ofImage> rightAnimframes;
    ofImage temp;
	for(int i=0; i<3; i++){
        temp.cropFrom(img1, i*128, 0, 128, 128);
        rightAnimframes.push_back(temp);
    }
	anim = new Animation(10,rightAnimframes);

}
void SelectState::tick() {
    pacmanButton->tick();
    msPacmanButton->tick();
    jrPacmanButton->tick();
    pacmaniaButton->tick();
	backButton->tick();
	anim->tick();
    if(pacmanButton->wasPressed()){
		setFinished(true);
		setNextState("Game");
		playerSelected = 0;
	}
    else if(msPacmanButton->wasPressed()){
		setFinished(true);
		setNextState("Game");
		playerSelected = 1;
	}
    else if(jrPacmanButton->wasPressed()){
		setFinished(true);
		setNextState("Game");
		playerSelected = 2;
	}
    else if(pacmaniaButton->wasPressed()){
		setFinished(true);
		setNextState("Game");
		playerSelected = 3;
	}
    else if(backButton->wasPressed()){
		setFinished(true);
		setNextState("Menu");
	}
}

void SelectState::setSprite(int spritesheet) { playerSelected = spritesheet; }
int SelectState::getSprite() { return playerSelected; }

void SelectState::render() {
	string title = "Character Select";
	ofDrawBitmapString(title, ofGetWidth()/2 - (4*title.size() - 2), ofGetHeight()/2-300, 50);
	ofSetBackgroundColor(0, 0, 0);
	ofSetColor(256, 256, 256);
	anim->getCurrentFrame().draw(ofGetWidth()/2-64, ofGetHeight()/2-128, 128, 128);
    pacmanButton->render();
    msPacmanButton->render();
    jrPacmanButton->render();
    pacmaniaButton->render();
    backButton->render();
}

void SelectState::keyPressed(int key){
	
}

void SelectState::mousePressed(int x, int y, int button){
    pacmanButton->mousePressed(x, y);
    msPacmanButton->mousePressed(x, y);
    jrPacmanButton->mousePressed(x, y);
    pacmaniaButton->mousePressed(x, y);
	backButton->mousePressed(x, y);
}

void SelectState::reset(){
	setFinished(false);
	setNextState("");
    pacmanButton->reset();
    msPacmanButton->reset();
    jrPacmanButton->reset();
    pacmaniaButton->reset();
	backButton->reset();
}

SelectState::~SelectState(){
	delete pacmanButton;
	delete msPacmanButton;
	delete jrPacmanButton;
	delete pacmaniaButton;
	delete backButton;
	delete anim;
}