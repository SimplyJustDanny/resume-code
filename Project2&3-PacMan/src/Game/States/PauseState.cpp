#include "PauseState.h"

PauseState::PauseState(){
    resumeButton = new Button(140,ofGetHeight()-240, 200, 180, "Resume");
    quitButton = new Button(ofGetWidth()-340,ofGetHeight()-240, 200, 180, "Quit");
}

void PauseState::tick(){
    resumeButton->tick();
    if(resumeButton->wasPressed()){
        setFinished(false);
        setNextState("Game");
    }
    else if(quitButton->wasPressed()){
        setFinished(true);
        ofExit();
    }
}

void PauseState::render(){
    ofSetBackgroundColor(0,0,0);
    ofColor(0,0,256);
    ofDrawBitmapString("Game is paused", ofGetWidth()/2 - 100, ofGetHeight()/2);
    resumeButton->render();
    quitButton->render();
}

void PauseState::keyPressed(int key){
    if (key=='p'){
        setFinished(false);
		setNextState("Game");
	}
}

void PauseState::mousePressed(int x, int y, int button){
    resumeButton->mousePressed(x,y);
    quitButton->mousePressed(x,y);
}

void PauseState::reset()
{
    setFinished(true);
    setNextState("");
    resumeButton->reset();
    quitButton->reset();
}