#include "GameOverState.h"

GameOverState::GameOverState() {
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
void GameOverState::tick() {
	startButton->tick();
	anim->tick();
	if(startButton->wasPressed()){
		setNextState("Game");
		setFinished(true);

	}
}
void GameOverState::render() {
	string title = "Game Over";
	ofDrawBitmapString(title, ofGetWidth()/2 - (4*title.size() - 10), ofGetHeight()/2-300, 50);
	ofDrawBitmapString("Score: " + to_string(score), ofGetWidth()/2, ofGetHeight()/2-138, 50);
	ofSetBackgroundColor(0, 0, 0);
	ofSetColor(256, 256, 256);
	anim->getCurrentFrame().draw(ofGetWidth()/2-64, ofGetHeight()/2-128, 128, 128);
	startButton->render();


}

void GameOverState::keyPressed(int key){
	
}

void GameOverState::mousePressed(int x, int y, int button){
	startButton->mousePressed(x, y);
}

void GameOverState::reset(){
	setFinished(false);
	setNextState("");
	startButton->reset();
}

void GameOverState::setScore(int sc){
    score = sc;
}

GameOverState::~GameOverState(){
	delete startButton;
	delete anim;
}