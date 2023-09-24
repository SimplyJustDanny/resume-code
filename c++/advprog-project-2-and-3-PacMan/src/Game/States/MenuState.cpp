#include "MenuState.h"

MenuState::MenuState() {
	startButton = new Button(ofGetWidth()/2-32, ofGetHeight()/2, 64, 50, "Start");
	img1.load("images/pacman-title.png");
	vector<ofImage> rightAnimframes;
    ofImage temp;
	for(int i=0; i<3; i++){
        temp.cropFrom(img1, i*128, 0, 128, 128);
        rightAnimframes.push_back(temp);
    }
	anim = new Animation(10,rightAnimframes);

}
void MenuState::tick() {
	startButton->tick();
	anim->tick();
	if(startButton->wasPressed()){
		setNextState("Select");
		setFinished(true);
	}
}
void MenuState::render() {
	string title = "Justin and Dan's Bustin' Pac-Man";
	ofDrawBitmapString(title, ofGetWidth()/2 - (4*title.size() - 10), ofGetHeight()/2-300, 50);
	ofSetBackgroundColor(0, 0, 0);
	ofSetColor(256, 256, 256);
	anim->getCurrentFrame().draw(ofGetWidth()/2-64, ofGetHeight()/2-128, 128, 128);
	startButton->render();
}

void MenuState::keyPressed(int key){
	
}

void MenuState::mousePressed(int x, int y, int button){
	startButton->mousePressed(x, y);
}

void MenuState::reset(){
	setFinished(false);
	setNextState("");
	startButton->reset();
}

MenuState::~MenuState(){
	delete startButton;
	delete anim;
}