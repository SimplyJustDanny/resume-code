#include "UltimatePowerup.h"

void UltimatePowerup::activate(Player *player){
    vector<Powerup*> pC = player->getPowerupsCollected();
    for (int i = 1; i < (int)pC.size(); i++) {
        int idx = i;
        while ((idx > 0) && (pC[idx]->compareTo(pC[idx - 1]) < 0)) {
            Powerup* swapPowerup = pC[idx];
            pC[idx] = pC[idx - 1];
            pC[idx - 1] = swapPowerup;
            idx--;
        }
    }
    player->setPowerupsCollected(pC);
}