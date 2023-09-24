
#include "Player.h"
#include "EntityManager.h"
#include "Dot.h"
#include "BigDot.h"
#include "Ghost.h"
#include "SpeedPowerup.h"
#include "CherryPowerUp.h"
#include "Cherry.h"
#include "StrawberryPowerup.h"
#include "Strawberry.h"
#include "RandomPowerUp.h"
#include "Apple.h"
#include "Orange.h"
#include "UltimatePowerup.h"
#include "Galaga.h"
#include "GhostEyes.h"

Player::Player(int x, int y, int width, int height, EntityManager* em, int pS) : Entity(x, y, width, height){
    spawnX = x;
    spawnY = y;
    //Pac-Man Skin Selector
    playerSelected = pS;
    switch(playerSelected){
        case 0:
            sprite.load("images/pacman.png");
            break;
        case 1:
            sprite.load("images/mspacman.png");
            break;
        case 2:
            sprite.load("images/jrpacman.png");
            break;
        case 3:
            sprite.load("images/pacmania.png");
            break;
        default:
            sprite.load("images/pacman.png");
            break;
    };

    down.cropFrom(sprite, 0, 48, 16, 16);
    up.cropFrom(sprite, 0, 32, 16, 16);
    left.cropFrom(sprite, 0, 16, 16, 16);
    right.cropFrom(sprite, 0, 0, 16, 16);

    vector<ofImage> downAnimframes;
    vector<ofImage> upAnimframes;
    vector<ofImage> leftAnimframes;
    vector<ofImage> rightAnimframes;
    ofImage temp;
    for(int i=0; i<3; i++){
        temp.cropFrom(sprite, i*16, 48, 16, 16);
        downAnimframes.push_back(temp);
    }
    for(int i=0; i<3; i++){
        temp.cropFrom(sprite, i*16, 32, 16, 16);
        upAnimframes.push_back(temp);
    }
    for(int i=0; i<3; i++){
        temp.cropFrom(sprite, i*16, 16, 16, 16);
        leftAnimframes.push_back(temp);
    }
    for(int i=0; i<3; i++){
        temp.cropFrom(sprite, i*16, 0, 16, 16);
        rightAnimframes.push_back(temp);
    }
    walkDown = new Animation(1,downAnimframes);
    walkUp = new Animation(1,upAnimframes);
    walkLeft = new Animation(1,leftAnimframes);
    walkRight = new Animation(1,rightAnimframes);

    this->em = em;

    moving = MLEFT;
    originalEntities = em->entities;
    //This ensures Speed is always in the vector
    Powerup *speed = new SpeedPowerup;  
    dynamic_cast<SpeedPowerup*>(speed);
    powerupsCollected.push_back(speed);       
}

void Player::tick(){
    checkCollisions();

    //Cherry Powerup failsafe (On the very rare occurence it does fail)
    if((x < 200 || x > 823) || (y < 64 || x > 823)){
        Powerup *teleport = new CherryPowerUp;
        dynamic_cast<CherryPowerUp *>(teleport);
        teleport->activate(this);
    }

    if (score >= 1000 && !galagaSpawn){
        ofImage galagaSpriteSheet;
        galagaSpriteSheet.load("images/Background.png");
        Galaga *galagaEnt = new Galaga(504,432,16,16, galagaSpriteSheet);
        em->entities.push_back(galagaEnt);
        galagaSpawn = true;
    }

    if (moving == MUP && canMoveUp) 
        facing = UP;
    else if (moving == MDOWN && canMoveDown) 
        facing = DOWN;
    else if (moving == MLEFT && canMoveLeft) 
        facing = LEFT;
    else if (moving == MRIGHT && canMoveRight)
        facing = RIGHT;

    if(facing == UP && canMoveUp){
        y-= speed;
        walkUp->tick();
    }else if(facing == DOWN && canMoveDown){
        y+=speed;
        walkDown->tick();
    }else if(facing == LEFT && canMoveLeft){
        x-=speed;
        walkLeft->tick();
    }else if(facing == RIGHT && canMoveRight){
        x+=speed;
        walkRight->tick();
    }
}

// Find Powerup function (Has to be here or else GPS won't work)
void Player::findPowerup(int powX, int powY, int outX, int outY, int tms, string dir){
    bool canMove = true;
    if (tms == 0 || (x == powX && y == powY)){
        ofNoFill();
        ofFill();
    }
    else{
        if (outX > powX && canMove){
            for(BoundBlock* boundBlock: em->boundBlocks){
                if(this->getBounds(outX-16, outY).intersects(boundBlock->getBounds())){
                    canMove = false;
                    break;
                }
            }
            if (canMove){
                findPowerup(powX, powY, outX-16, outY, tms - 1, "left");
                canMove = false;
            }
            else{
                canMove = true;
            }
        }
        if (outX < powX && canMove){
            for(BoundBlock* boundBlock: em->boundBlocks){
                if(this->getBounds(outX+16, outY).intersects(boundBlock->getBounds())){
                    canMove = false;
                    break;
                }
            }
            if (canMove){
                findPowerup(powX, powY, outX+16, outY, tms - 1, "right");
                canMove = false;
            }
            else{
                canMove = true;
            }
        }
        if (outY == powY && canMove){
            if(dir.compare("down") == 0)
                findPowerup(powX, powY, outX, outY-16, tms - 1, "down");
            else{ 
                findPowerup(powX, powY, outX, outY+16, tms - 1, "up");
            }
            canMove = false;
        }
        if (outY > powY && canMove){
            for(BoundBlock* boundBlock: em->boundBlocks){
                if(this->getBounds(outX, outY-16).intersects(boundBlock->getBounds())){
                    canMove = false;
                    break;
                }
            }
            if (canMove){
                findPowerup(powX, powY, outX, outY-16, tms - 1, "down");
                canMove = false;
            }
            else{
                canMove = true;
            }
        }
        if (outY < powY && canMove){
            for(BoundBlock* boundBlock: em->boundBlocks){
                if(this->getBounds(outX, outY+16).intersects(boundBlock->getBounds())){
                    canMove = false;
                    break;
                }
            }
            if (canMove){
                findPowerup(powX, powY, outX, outY+16, tms - 1, "up");
                canMove = false;
            }
            else{
                canMove = true;
            }
        }
        if (outX == powX && canMove){
            if (dir.compare("left") == 0){
                findPowerup(powX, powY, outX-16, outY, tms - 1, "left");
            }
            else{
                findPowerup(powX, powY, outX+16, outY, tms - 1, "right");
            }
            canMove = false;
        }
    }
    ofNoFill();
	ofDrawCircle(outX+8, outY+8, 8);
    ofFill();
}

void Player::render(){

    //Boolean for Strawberry Powerup
    if (evade == false){
    ofSetColor(256,256,256);
    // ofDrawRectangle(getBounds());
        if(facing == UP)
            walkUp->getCurrentFrame().draw(x, y, width, height);
        else if(facing == DOWN)
            walkDown->getCurrentFrame().draw(x, y, width, height);
        else if(facing == LEFT)
            walkLeft->getCurrentFrame().draw(x, y, width, height);
        else if(facing == RIGHT)
            walkRight->getCurrentFrame().draw(x, y, width, height);
    }
    else{
        ofSetColor(0,0,0);
        timer += 1;
        if (timer == 15){
            timer = 0;
            setEvade(false);
        }
    }

    ofSetColor(256, 0, 0);
    ofDrawBitmapString("Health: ", ofGetWidth()/2 + 125, 50);

    for(unsigned int i=0; i<health; i++){
        ofDrawCircle(ofGetWidth()/2 + 25*i +200, 50, 10);
    }
    ofDrawBitmapString("Score: "  + to_string(score), ofGetWidth()/2-224, 50);

    //Displays Name of Selected Character
    switch(playerSelected){
        case 0:
            playerDisplay = "Pac-Man";
            break;
        case 1:
            playerDisplay = "Ms. Pac-Man";
            break;
        case 2:
            playerDisplay = "Jr. Pac-Man";
            break;
        case 3:
            playerDisplay = "Pac-Mania";
            break;
        default:
            //This was crucial in understanding why ChoosePlayerState wasn't working
            playerDisplay = to_string(playerSelected);
            break;
    };
	ofDrawBitmapString(playerDisplay, ofGetWidth()/2 - 300, 50);

    // Displays Pacman's cordinates for debugging purposes
    ofDrawBitmapString("(" + to_string(x) + "," + to_string(y) + ")", ofGetWidth()/2 - 300, 30);

    // This displays your powerups (+ the number of powerups) in your vector via rank
    for (Powerup* pointer: powerupsCollected){
        if (int(powerupList.find(to_string(pointer->getRank()))) == -1){
            powerupList = powerupList + " " + to_string(pointer->getRank());
        }
    }
    ofDrawBitmapString("Powerup Ranks:" + powerupList + " (" + to_string(powerupsCollected.size()) +")", ofGetWidth()/2 - 108, 50);

    //GPS Function
    if (activeGPS){
        // This checks roughly the nearest poweruo
        if (x == distX && y == distY){
            distX = 9999;
            distY = 9999;
        }
        for (Entity* ents: em->entities){
            if (dynamic_cast<Apple *>(ents) || dynamic_cast<Cherry *>(ents) || dynamic_cast<Galaga *>(ents) || dynamic_cast<Orange *>(ents) || dynamic_cast<Strawberry *>(ents)){
                if (sqrt(pow((ents->getX() - this->x),2)+pow((ents->getY() - this->y),2)) < sqrt(pow((distX - this->x),2)+pow((distY - this->y),2))){
                    distX = ents->getX();
                    distY = ents->getY();
                }
            }
        }

        if (distX == 9999 && distY == 9999){
            // Text that means no more powerups basically
            ofDrawBitmapString("GPS Active (N/A)",ofGetWidth()/2 - 108, 30);
        }
        else{
		    //Calls for the findPowerup function
		    findPowerup(distX,distY,((((this->x+8)/16)*16)-8),((this->y/16)*16), 75, "null");
            // Nearest powerup cordinates for debugging purposes 
            ofDrawBitmapString("GPS Active (" + to_string(distX) + "," + to_string(distY) + ")",ofGetWidth()/2 - 108, 30);
        }
    }
}

void Player::keyPressed(int key){
    switch(key){
        case 'w':
            moving = MUP;
            break;
        case 's':
            moving = MDOWN;
            break;
        case 'a':
            moving = MLEFT;;
            break;
        case 'd':
            moving = MRIGHT;;
            break;
        case 'n':
            die();
            break;
        case 'm':
            if (this->getHealth() < 3){
                health++;
            }
            break;
        case ' ':
            powerupsCollected[powerupsCollected.size()-1]->activate(this);
            if(powerupsCollected.size() == 1){ // This is to ensure Speed (or at least one powerup) is always in the vector
                break;
            }
            powerupsCollected.pop_back();
            // Resetting the list allows it to update properly
            powerupList = "";
            break;
        case '1':
            activeGPS = !activeGPS;
            break;
    };
};

void Player::keyReleased(int key){
    if(key == 'w' || key =='s' || key == 'a' || key == 'd'){
        walking = false;
    }
}
void Player::mousePressed(int x, int y, int button){
}

int Player::getHealth(){ return health; }
int Player::getScore(){ return score; }
int Player::getSpeed(){ return speed; }
FACING Player::getFacing(){ return facing; }
vector<Powerup*> Player::getPowerupsCollected(){ return powerupsCollected; }
void Player::setHealth(int h){ health = h; }
void Player::setFacing(FACING facing){ this->facing = facing; }
void Player::setScore(int h){ score = h; }
void Player::setSpeed(int h){ speed = h; }
void Player::setEvade(bool h){ evade = h; }
void Player::setPowerupsCollected(vector<Powerup*> h) { powerupsCollected = h;}

void Player::checkCollisions(){
    canMoveUp = true;
    canMoveDown = true;
    canMoveLeft = true;
    canMoveRight = true;

    for(BoundBlock* boundBlock: em->boundBlocks){
        if(this->getBounds(x, y-speed).intersects(boundBlock->getBounds())){
            canMoveUp = false;
            if (y % 16 != 0){ y -= (y % 16); } // This bit makes turning corners with Speed Powerup possible
        }
        if(this->getBounds(x, y+speed).intersects(boundBlock->getBounds())){
            canMoveDown = false;
            if (y % 16 != 0){ y += ((16 - (y % 16)) % 16); } // See comment above
        }   
        if(this->getBounds(x-speed, y).intersects(boundBlock->getBounds())){
            canMoveLeft = false;
            if ((x + 8) % 16 != 0){ x -= ((x + 8) % 16); } // See comment above
        }
        if(this->getBounds(x+speed, y).intersects(boundBlock->getBounds())){
            canMoveRight = false;
            if ((x + 8) % 16 != 0){ x += ((16 - ((x + 8) % 16)) % 16); } // See comment above
        }
        // In case Pacman got stuck somewhere
        if(this->getBounds(x, y).intersects(boundBlock->getBounds())){
            Powerup *teleport = new CherryPowerUp;
            dynamic_cast<CherryPowerUp *>(teleport);
            teleport->activate(this);
        }
    }
    for(Entity* entity:em->entities){
        // Deals with spawning ghost eyes
        GhostEyes *checkRemoveEyes = dynamic_cast<GhostEyes *>(entity);
        if(checkRemoveEyes != nullptr && checkRemoveEyes->getRemove()){
            entity->remove = true;
            isNewGhost = true;
        }
        if(collides(entity)){
            if (dynamic_cast<GhostEyes *>(entity)){
                entity->remove = false;
            }
            if (dynamic_cast<Cherry *>(entity)){
                entity->remove = true;
                Powerup *teleport = new CherryPowerUp;
                dynamic_cast<CherryPowerUp *>(teleport);
                powerupsCollected.push_back(teleport);
            }
            if(dynamic_cast<Apple*>(entity) || dynamic_cast<Orange*>(entity)){
                entity->remove = true;
                Powerup *random = new RandomPowerUp;
                dynamic_cast<RandomPowerUp *>(random);
                random->activate(this);
            }
            if(dynamic_cast<Strawberry *>(entity)){
                entity->remove = true;
                Powerup *vanish = new StrawberryPowerup;
                dynamic_cast<StrawberryPowerup*>(vanish);
                powerupsCollected.push_back(vanish);
            }
            if(dynamic_cast<Galaga *>(entity)){
                entity->remove = true;
                Powerup *sort = new UltimatePowerup;
                dynamic_cast<UltimatePowerup*>(sort);
                sort->activate(this);
                powerupList = "";
            }
            if(dynamic_cast<Dot*>(entity) || dynamic_cast<BigDot*>(entity)){
                entity->remove = true;
                score += 10;
            }
            if(dynamic_cast<BigDot*>(entity)){
                score +=20;
                em->setKillable(true);
            }
        }
    }
    for(Entity* entity:em->ghosts){
        if(collides(entity)){
            Ghost* ghost = dynamic_cast<Ghost*>(entity);
            if(ghost->getKillable()){
                ghost->remove = true;
                ghostEyesImg.load("images/Background.png");
                GhostEyes *eyes = new GhostEyes(ghost->getX(), ghost->getY(), 16, 16, ghostEyesImg);
                eyes->setCoords(ghost->getCoords());
                em->entities.push_back(eyes);
            }
            else if (evade == false)
                die();
        }
    }
}

int Player::getDotSize() {return em->entities.size();}

// Die
void Player::die(){
    health--;
    x = spawnX;
    y = spawnY;
}

Player::~Player(){
    delete walkUp;
    delete walkDown;
    delete walkLeft;
    delete walkRight;
}

void Player::setX(int newX) {this->x = newX;}
void Player::setY(int newY) {this->y = newY;}
vector<Entity*> Player::getOriginalEntities() {return originalEntities;}
void Player::setNewGhost(bool isNew) { this->isNewGhost = isNew; }
bool Player::getNewGhost() { return isNewGhost; }