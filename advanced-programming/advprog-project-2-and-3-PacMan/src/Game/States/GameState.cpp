#include "GameState.h"
#include "Entity.h"

GameState::GameState(int pS) {
	playerSelected = pS;
	music.load("music/pacman_chomp.wav");
	mapImage.load("images/map1.png");
	map = MapBuilder().createMap(mapImage, playerSelected);
}
void GameState::tick() {
	if(!music.isPlaying()){
			music.play();
	}
	map->tick();
	if(map->getPlayer()->getDotSize()==0){
		setFinished(true);
		setNextState("Win");
		map->getPlayer()->setHealth(3);
		finalScore = map->getPlayer()->getScore();
		map->getPlayer()->setScore(0);
		
	}
	if(map->getPlayer()->getHealth() == 0){
		setFinished(true);
		setNextState("over");
		map->getPlayer()->setHealth(3);
		finalScore = map->getPlayer()->getScore();
		map->getPlayer()->setScore(0);
	}
	if(map->getPlayer()->getNewGhost()){
		map->getGhostSpawner()->setNewGhost(true);
		map->getPlayer()->setNewGhost(false);
	}
}
void GameState::render() {
	map->render();
}

void GameState::keyPressed(int key){
	if(key=='y') {
		setFinished(true);
		setNextState("Win");
		map->getPlayer()->setHealth(3);
		finalScore = map->getPlayer()->getScore();
		map->getPlayer()->setScore(0);
	}
	if (key=='p') {
		setPaused(true);
		setFinished(false);
		setNextState("Pause");
	}
	map->keyPressed(key);
}

void GameState::mousePressed(int x, int y, int button){
	map->mousePressed(x, y, button);
}

void GameState::keyReleased(int key){
	map->keyReleased(key);
}

void GameState::reset(){
	setFinished(false);
	setNextState("");
}

int GameState::getFinalScore(){
	return finalScore;
}

GameState::~GameState(){
	delete map;
}