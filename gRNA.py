# Jason Dean
# 12/28/2016
#
# A program to find sgRNA sequences
#
# Please install Biopython to use this program:  http://biopython.org/wiki/Download
#
# This program accepts the following command line arguments:
# python gRNA.py Target_Sequence(required) Reference_Sequence(optional)
#
# Target_Sequence:  the DNA sequence to be targeted by CRISPR in FASTA format
#
# Reference_Sequence:  the reference sequence that gRNA sequences
# will be evaluated against for off target binding.  Please only provide the taxid number
# as input for the reference sequence.
#
#   Example:  Synechococcus elongatus PCC 7942 (taxid:1140)
#   provide '1140' as reference sequence input.
#
#   More information can be found here:  https://www.ncbi.nlm.nih.gov/taxonomy
# ____________________________________________________________________________________________________

import sys
import eBLAST

# _______________________________ Variables __________________________________________
targetFile = None # file handle for input gene/region to be targeted
gRNA_list = [] #li


# _______________________________ Processing __________________________________________

# create a sgRNA class
class sgRNA(object):

    # count the number of gRNAs in the class
    counter = 0

    def __init__(self, gRNA="", gcContent="", eScore1=0, eScore2=0):
        self.gRNA = gRNA
        self.gcContent = gcContent
        self.eScore1 = eScore1
        self.eScore2 = eScore2
        sgRNA.counter += 1

# find gRNA sequences based on proximity to PAM sequence
def gRNAs(target, gRNA_list):

    # we only consider gRNA targets that occur in the first quarter of the target sequence
    for i in range(21, int(len(target)/4)):
        PAM = target[i:(i+2)]
        if PAM == 'gg':
            gRNA = target[(i-21):(i-1)]

            # on add target to list if GC content is between 20 and 80%
            if GC(gRNA):
                gRNA_list.append(sgRNA(gRNA, GC(gRNA)))
    return gRNA_list


# compute the 5' to 3' reverse complement of the target sequence
def reverseComplement(target):

    targetRev = ''

    length = len(target)
    for i in range(len(target)):

        if target[length-1] == 'a':
            add = 't'
        elif target[length-1] == 't':
            add = 'a'
        elif target[length-1] == 'c':
            add = 'g'
        else:
            add = 'c'

        targetRev = targetRev + add
        length += -1

    return targetRev

# determine the GC content of a DNA sequence
def GC(seq):
    g = seq.count('g')
    c = seq.count('c')
    gc = (g+c)/len(seq)
    if gc > 0.4 and gc < 0.8:
        return gc
    else:
        return False

# out put the gRNA list to a txt file
def Output(gRNA_List, ref=True):
    gRNAfasta = open("sgRNA.txt", "w+")
    counter = 1
    for i in gRNA_List:
        gc = "gc: {0}, ".format(i.gcContent)
        eScore = "eScore1: {0}, eScore2: {1}".format(i.eScore1, i.eScore2)

        gRNAfasta.write(">gRNA_" + str(counter) + "\n" + i.gRNA + "\n" + gc + eScore + "\n\n")
        counter += 1


# _______________________________ Input and Output __________________________________________
#import the CRISPR target sequence
try:
    #open the target sequence
    targetFile = open(sys.argv[1], 'r')
    #split the FASTA sequence into the name and sequence
    name, target = targetFile.read().split('\n',1)
    target = target.lower().replace('\n', '')
    print("\nsequence to be targeted:  ", name)
except Exception as e:
    print("Error reading target sequence: " + str(e) + "\n")

#import the reference sequence, if provided
try:
    #open the reference sequence
    reference = sys.argv[2]
    print("\nReference sequence to be used: ", sys.argv[2], "\n")
    ref = True
except Exception as e:
    print("\nNo reference sequence provided\n")
    ref = False

#create a list of potential gRNAs
# noncoding strand
gRNA_list = gRNAs(target, gRNA_list)

# coding strand
targetRev = reverseComplement(target)
gRNA_list = gRNAs(targetRev, gRNA_list)

# BLAST the sgRNA candidates and get the eScores of the top two hits
if ref:
    print("Blasting candidate gRNA sequences.  Please wait...")
    gRNA_list = eBLAST.eBLAST_List(gRNA_list, reference)
    Output(gRNA_list, ref)
else:
    Output(gRNA_list, ref)

print("Complete. Data has been written to :  sgRNA.txt. \n\n"
      "Summary:  \nnumber of gRNAs:  ", sgRNA.counter, "\n")
for i in gRNA_list:
    print(i.gRNA, i.gcContent, i.eScore1, i.eScore2)