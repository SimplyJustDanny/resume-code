# NES Project

To build assembly file, make sure you have both ca65 and ld65 installed.
Afterwards, run the following on the command line (remember to change directory):
ca65 nesproject.s
ld65 nesproject.o -t nes -o nesproject.nes