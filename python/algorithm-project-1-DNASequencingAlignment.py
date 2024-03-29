#Sys importing that handles terminal inputs
import sys
if len(sys.argv) > 1:
    #Establish helper function to take the three scores values and picks the highest.
    def maxim(dscore, xscore, yscore):
        if (yscore > xscore): xscore = yscore
        if (dscore > xscore): return dscore
        return xscore
    #Make file handler for processing the terminal input.
    files = open(sys.argv[1], "r")
    #Get rid of sequence1,sequence2 header
    files.readline()
    #Iterate through each line in the file.
    for lines in files:
        #Stores both inputs to be aligned.
        inpt1 = lines.split(",")[0]
        inpt2 = lines.split(",")[1].strip()
        #Initializes the score and direction matrix [x/j = input 2 length, y/i = input 1 length].
        matrx = [[0]*(len(inpt2) + 1) for i in range(len(inpt1) + 1)]
        drect = [[" "]*(len(inpt2) + 1) for i in range(len(inpt1) + 1)]
        for i in range(len(matrx)):
            matrx[i][0] = -2*i
        for j in range(len(matrx[0])):
            matrx[0][j] = -2*j
        #Establish gap penalty.
        gap = -2
        #Iterates through both matrixes.
        for i in range(1, len(matrx)):
            for j in range(1, len(matrx[i])):
                #Set score to -1, becomes 1 if inputs on respective indexes are the same letter.
                score = -1
                if (inpt2[j-1] == inpt1[i-1]): score = 1
                #Calculates adjacent cells' scores and yields maximum to place in score matrix.
                dcell = matrx[i-1][j-1]+score
                xcell = matrx[i][j-1]+gap
                ycell = matrx[i-1][j]+gap
                mxmum = maxim(dcell, xcell, ycell)
                matrx[i][j] = mxmum
                #Checks which value is maximum, with up-left-diagonal bias, to then place respective direction in direction matrix.
                if mxmum == ycell: drect[i][j] = "u"
                elif mxmum == xcell: drect[i][j] = "l"
                else: drect[i][j] = "d"
        #We are now out of matrix loop, which means both matrixes are done, time to set up outputs to build upon.
        oupt1 = ""
        oupt2 = ""
        score = matrx[len(inpt1)][len(inpt2)]
        #Setting up iterator variables to backtrack through our direction matrix.
        y = len(inpt1)
        x = len(inpt2)
        #While loop with iterators to build the alignment of each output backwards.
        while y > 0 or x > 0:
            #Variable of the current direction shell for comparison.
            dir = drect[y][x]
            #Diagonal? Subtract indexes and add in the next characters of both outputs.
            if dir == "d":
                y -= 1
                x -= 1
                oupt1 = inpt1[y] + oupt1
                oupt2 = inpt2[x] + oupt2
            #Upward? Subtract y, add next character for output 1 and add filler for output 2.
            elif dir == "u":
                y -= 1
                oupt1 = inpt1[y] + oupt1
                oupt2 = "-" + oupt2
            #Leftward? Subtract x, add filler for output 1 and add next character for output 2.
            elif dir == "l":
                x -= 1
                oupt1 = "-" + oupt1
                oupt2 = inpt2[x] + oupt2
            #If we arrived here, it means that one of our iterators is now zero.
            else:
                #If remaining iterator is y, add remaining letters to output 1 and filler to output 2.
                if y > 0:
                    y -= 1
                    oupt1 = inpt1[y] + oupt1
                    oupt2 = "-" + oupt2
                #If remaining iterator is x, add filler to output 1 and remaining letters to output 2.
                if x > 0:
                    x -= 1
                    oupt1 = "-" + oupt1
                    oupt2 = inpt2[x] + oupt2
        #We are done building the outputs. Print output and continue with next line.
        print(oupt1, oupt2, score)
    #Done with all lines. Don't forget to close your files, kids!
    files.close()