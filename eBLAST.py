# Jason Dean
# 12/28/2016
# This module will blast DNA sequences from a list against a reference
# sequence and adds the eScores of the top two most significant hits for each
# DNA sequence to the list

if __name__ == "__main__":
     raise Exception("this program is meant to be imported")

from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML

def eBLAST_List(gRNA_List, refSeq):

     refSeq = 'txid' + refSeq + '[ORGN]'

     # convert gRNA_List to a FASTA file
     gRNAfasta = open("sgRNA.txt", "w+")
     counter = 1
     for i in gRNA_List:
          gRNAfasta.write(">gRNA_" + str(counter) + "\n" + i.gRNA + "\n\n")
          counter += 1

     gRNAfasta.seek(0)
     gRNAread = gRNAfasta.read()

     # BLAST the gRNAs against the ref sequence
     result_handle=NCBIWWW.qblast('blastn', 'nt', gRNAread, entrez_query="txid1140[ORGN]", hitlist_size=2)

     # parse the BLAST result XML file
     blast_record = NCBIXML.parse(result_handle)

     # obtain the eScores of the top two most significant hits
     counter = 0
     eList = []
     eTemp = []
     for results in blast_record:
          for alignment in results.alignments:
               for hsp in alignment.hsps:

                    eTemp.append(hsp.expect)

          gRNA_List[counter].eScore1 = eTemp[0]
          gRNA_List[counter].eScore2 = eTemp[1]

          eList.append(eTemp[1])
          eTemp = []
          counter += 1

     # return a gRNA list containing eScores
     return gRNA_List