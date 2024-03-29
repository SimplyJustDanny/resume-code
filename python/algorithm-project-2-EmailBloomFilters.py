#Array importing so I can make bit arrays
import array
#Math importing so I can do logs
import math
#Sys importing that handles terminal inputs
import sys
if len(sys.argv) > 1:
    #Establish bit array functions, provided by Wilfredo Lugo.
    #makeBitArray() is self-explanatory, creating a bit array of n size.
    def makeBitArray(bitSize, fill = 0):
        intSize = bitSize >> 5                   # number of 32 bit integers
        if (bitSize & 31):                      # if bitSize != (32 * n) add
            intSize += 1                        #    a record for stragglers
        if fill == 1:
            fill = 4294967295                                 # all bits set
        else:
            fill = 0                                      # all bits cleared
        bitArray = array.array('I')          # 'I' = unsigned 32-bit integer
        bitArray.extend((fill,) * intSize)
        return(bitArray)
    #setBit() returns an integer with the bit at 'bit_num' set to 1.
    def setBit(array_name, bit_num):
        record = bit_num >> 5
        offset = bit_num & 31
        mask = 1 << offset
        array_name[record] |= mask
        return(array_name[record])
    #testBit() returns a nonzero result, 2**offset, if the bit at 'bit_num' is set to 1.
    def testBit(array_name, bit_num):
        record = bit_num >> 5
        offset = bit_num & 31
        mask = 1 << offset
        return(array_name[record] & mask)
    #Make file handler for processing the first terminal input, to construct filter.
    file1 = open(sys.argv[1], "r")
    #Get rid of the email header.
    file1.readline()
    #Convert file into a list in order to extract list size for calculating filter size.
    elist = file1.readlines()
    #We've already extracted the list, so we can close the first input file.
    file1.close()
    #Generate filter size with given formula.
    fsize = int(math.ceil((len(elist) * math.log(0.0000001)) / math.log(1 / pow(2, math.log(2)))))
    #Now generate the number of hases to make.
    hashs = int(round((fsize / float(len(elist))) * math.log(2)))
    #Finally, we start construction on the bloom filter.
    filtr = makeBitArray(fsize)
    #Iterate through each email in the construct list.
    for email in elist:
        #Strips the current email of any newlines for input.
        input = email.strip()
        #For every number in the range of the hash, we add it to the input to create "new" hash functions.
        for i in range(hashs):
            setBit(filtr,(hash(input + str(i)) % fsize))
    #Filter complete. Make file handler for processing the second terminal input, to check filter.
    file2 = open(sys.argv[2], "r")
    #Once again getting rid of email header.
    file2.readline()
    #Iterate through each line (emails) in the check file.
    for lines in file2:
        #Assume by default that the check is true.
        bloom = True
        #Strips the current line of newlines for output.
        outpt = lines.strip()
        #We check the hashes of each output using our given hash number
        for i in range(hashs):
            #If it turns out that any bit is zero, then we know the email is not in the filter and break.
            if (testBit(filtr,(hash(outpt + str(i)) % fsize)) == 0):
                bloom = False
                break
        #Check done. Print apprpriate output based on bloom boolean and move on to next line.
        if bloom: print(outpt + ",Probably in the DB")
        else: print(outpt + ",Not in the DB")
    #Done with all file 2 lines. Again, don't forget to close your files, kids!
    file2.close()