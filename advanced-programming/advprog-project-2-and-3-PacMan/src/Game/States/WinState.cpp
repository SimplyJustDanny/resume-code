#include "WinState.h"

WinState::WinState()
{
    restartButton = new Button(ofGetWidth() / 2 - 280, ofGetHeight() - 200, 200, 180, "Restart");
    mainMenuButton = new Button(ofGetWidth() / 2 + 40, ofGetHeight() - 200, 200, 180, "Menu");
    quitButton = new Button(ofGetWidth() / 2 - 100, ofGetHeight() - 200, 200, 180, "Quit");
}

void WinState::tick()
{
    restartButton->tick();
    mainMenuButton->tick();
    if (restartButton->wasPressed())
    {
        setFinished(true);
        setNextState("Game");
    }
    else if (mainMenuButton->wasPressed())
    {
        setFinished(true);
        setNextState("Menu");
    }
    else if (quitButton->wasPressed())
    {
        setFinished(true);
        ofExit();
    }
}

void WinState::setScore(int s) { finalScore = s; }

void WinState::render()
{
    ofSetBackgroundColor(0, 0, 0);
    ofColor(0, 0, 256);
    ofDrawBitmapString("You Win!!!", ofGetWidth() / 2 - 100, ofGetHeight() / 2 - 100);
    ofDrawBitmapString("Score: " + to_string(finalScore), ofGetWidth() / 2 - 100, ofGetHeight() / 2 - 50);
    restartButton->render();
    mainMenuButton->render();
    quitButton->render();
}

void WinState::keyPressed(int key)
{
}

void WinState::mousePressed(int x, int y, int button)
{
    restartButton->mousePressed(x, y);
    mainMenuButton->mousePressed(x, y);
    quitButton->mousePressed(x, y);
}

void WinState::reset()
{
    setFinished(false);
    setNextState("");
    restartButton->reset();
    mainMenuButton->reset();
    quitButton->reset();
}