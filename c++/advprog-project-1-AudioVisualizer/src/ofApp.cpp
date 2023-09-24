#include "ofApp.h"

//--------------------------------------------------------------
void ofApp::setup(){
    sound.loadSound("beat.wav"); //Loads a sound file (in bin/data/)
    sound.setLoop(true); // Makes the song loop indefinitely
    sound.setVolume(1); // Sets the song volume
    ofSetBackgroundColor(255, 128,0); // Sets the Background Color
    
}

//--------------------------------------------------------------
void ofApp::update(){
    /* The update method is called muliple times per second
    It's in charge of updating variables and the logic of our app */
    ofSoundUpdate(); // Updates all sound players
    visualizer.updateAmplitudes(); // Updates Amplitudes for visualizer
    vsize = recordkeys.size();
    if (replay){
        timer -= 1;
        if (i == vsize){
            i = 0;
            replay = false;
        }
        else if (timer == 0){
            keyPressed(recordkeys[i]);
            i += 1;
            timer = 180;
        }
    }
}

//--------------------------------------------------------------
void ofApp::draw(){
    /* The update method is called muliple times per second
    It's in charge of drawing all figures and text on screen */
    ofSetColor(256);
    ofDrawBitmapString("# of keys in recording: " + to_string(vsize) + ".",ofGetWidth() - 320,15);
    ofDrawBitmapString("Volume: " + to_string(sound.getVolume()) + ".",ofGetWidth() - 512,15);
    if(!playing){
        ofSetColor(256);
        ofDrawBitmapString("Press 'a' to play some music!", ofGetWidth()/2 - 50, ofGetHeight()/2);
    }
    vector<float> amplitudes = visualizer.getAmplitudes();
    if(mode == '1'){
        drawMode1(amplitudes);
    }else if(mode == '2'){
        drawMode2(amplitudes);
    }else if(mode == '3'){
        drawMode3(amplitudes);
    }else{
        ofSetColor(255,128,0);
    }
    if (rec == true){
        ofSetColor(256);
        ofDrawBitmapString("Recording is on.",ofGetWidth() - 320,30);
        std::cout << vsize << endl;
    }
    if (replay == true){
        ofSetColor(256);
        ofDrawBitmapString("Replaying recording. (" + to_string(vsize - i) + " keys left)",ofGetWidth() - 320,30);
    }
}

void ofApp::drawMode1(vector<float> amplitudes){
        ofFill(); // Drawn Shapes will be filled in with color
        if(playing){
            if (abs(red - 255) < 32){
            red = (red + 32) % 256;
            }
            if (abs(grn - 128) < 32){
            grn = (grn + 32) % 256;
            }
            if (abs(blu - 0) < 32){
            blu = (blu + 32) % 256;
            }
            ofSetColor(red, grn, blu);
        }
        else{
            ofSetColor(255,128,0);
            red = rand() % 256;
            grn = rand() % 256;
            blu = rand() % 256;
        }
        int size = amplitudes.size();
        int count = 2;
        for (int i=0; i < size;i++){
            ofDrawRectangle(count,ofGetHeight()-50,ofGetWidth() / 50, amplitudes[i] * 4);
            count += 17;
        }
        ofSetColor(256); // This resets the color of the "brush" to white
        ofDrawBitmapString("Rectangle Height Visualizer", 0, 15);
}
void ofApp::drawMode2(vector<float> amplitudes){
        ofSetLineWidth(5); // Sets the line width
        ofNoFill(); // Only the outline of shapes will be drawn
        int bands = amplitudes.size();
        for(int i=0; i< bands; i++){
            ofSetColor((bands - i)*32 %256,18,144); // Color varies between frequencies
            ofDrawCircle(ofGetWidth()/2, ofGetHeight()/2, amplitudes[0]/(i +1));
        }
        ofSetColor(256); // This resets the color of the "brush" to white
        ofDrawBitmapString("Circle Radius Visualizer", 0, 15);
}

void ofApp::drawMode3(vector<float> amplitudes){
    ofFill(); // Drawn Shapes will be filled in with color
    ofSetColor(256); // This resets the color of the "brush" to white
    if(playing){
        if (abs(red - 255) < 32){
            red = (red + 32) % 256;
        }
        if (abs(grn - 128) < 32){
            grn = (grn + 32) % 256;
        }
        if (abs(blu - 0) < 32){
            blu = (blu + 32) % 256;
        }
        ofSetColor(red, grn, blu);
        }
        else{
            ofSetColor(255,128,0);
            red = rand() % 256;
            grn = rand() % 256;
            blu = rand() % 256;
        }
        int size = amplitudes.size();
        int count = 2;
        for (int i=0; i < size;i++){
            ofDrawRectangle(0,count,amplitudes[i] * -4,ofGetHeight() / 50);
            count += 15;
        }
        ofSetColor(256);
        ofDrawBitmapString("Rectangle Width Visualizer", 0, 15);
}

//--------------------------------------------------------------
void ofApp::keyPressed(int key){
    if (rec == true && key != 'r' && key != 't'){
        recordkeys.push_back(key);
    }
    // This method is called automatically when any key is pressed
    if(!replay || (timer == 0)){
    switch(key){
        case 'a':
            if(playing){
                sound.stop();
            }else{
                sound.play();
            }
            playing = !playing;
            break;
        case '1':
            mode = '1';
            break;
            
        case '2':
            mode = '2';
            break;
        case '3':
            mode = '3';
            break;
        case 's':
            sound.loadSound("beat.wav");
            sound.setLoop(true);
            sound.setVolume(sound.getVolume());
            if(playing){
                red = rand() % 256;
                grn = rand() % 256;
                blu = rand() % 256;
                sound.play();
            }
            break;
        case 'd':
            sound.loadSound("geesebeat.wav");
            sound.setLoop(true);
            sound.setVolume(sound.getVolume());
            if(playing){
                red = rand() % 256;
                grn = rand() % 256;
                blu = rand() % 256;
                sound.play();
            }
            break;
        case 'f':
            sound.loadSound("pigeon-coo.wav");
            sound.setLoop(true);
            sound.setVolume(sound.getVolume());
            if(playing){
                red = rand() % 256;
                grn = rand() % 256;
                blu = rand() % 256;
                sound.play();
            }
            break;
        case 'g':
            sound.loadSound("rock-song.wav");
            sound.setLoop(true);
            sound.setVolume(sound.getVolume());
            if(playing){
                red = rand() % 256;
                grn = rand() % 256;
                blu = rand() % 256;
                sound.play();
            }
            break;
        case '=':
            if (sound.getVolume() < 1){
                sound.setVolume(sound.getVolume()+0.1);
            }
            break;
        case '-':
            if (sound.getVolume() > 0){
                if(sound.getVolume()-0.1 > 0){
                sound.setVolume(sound.getVolume()-0.1);
                }
                else{
                sound.setVolume(0);
                }
            }
            break;
        case ';':
            if (sound.getVolume() > 0){
                vol = sound.getVolume();
                sound.setVolume(0);
            }
            else{
                sound.setVolume(vol);
            }
            break;
        case 'r':
            rec = !rec;
            if (rec == true){
                recordkeys.clear();
            }
            break;
        case 't':
            if (!rec){
                replay = true;
            }
            break;
        }
    }   
    else{
    switch(key){
        case 'c':
            replay = false;
            timer = 180;
            i = 0;
            break;
        case 'v':
            replay = false;
            timer = 180;
            break;
        }
    }
}

//--------------------------------------------------------------
void ofApp::keyReleased(int key){

}

//--------------------------------------------------------------
void ofApp::mouseMoved(int x, int y){

}

//--------------------------------------------------------------
void ofApp::mouseDragged(int x, int y, int button){

}

//--------------------------------------------------------------
void ofApp::mousePressed(int x, int y, int button){

}

//--------------------------------------------------------------
void ofApp::mouseReleased(int x, int y, int button){

}

//--------------------------------------------------------------
void ofApp::mouseEntered(int x, int y){

}

//--------------------------------------------------------------
void ofApp::mouseExited(int x, int y){

}

//--------------------------------------------------------------
void ofApp::windowResized(int w, int h){

}

//--------------------------------------------------------------
void ofApp::gotMessage(ofMessage msg){

}

//--------------------------------------------------------------
void ofApp::dragEvent(ofDragInfo dragInfo){ 
}
