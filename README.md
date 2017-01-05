# gRNA

### Objective
This tool is designed to aid in selection and design of CRISPR Cas9 short guide RNAs (gRNA) that target a user provided sequence. 

### Background
Gene editing via [CRISPR Cas9](https://en.wikipedia.org/wiki/CRISPR#Cas9 "CRISPR") endonucleases has become a standard molecular biology lab technique for a wide variety of genetic engineering purposes.  A functional CRISPR Cas9 system includes the Cas9 endonuclease protein and a 20nt gRNA that directs Cas9 to a target DNA sequence.  The gRNA sequence must be immediately downstream of a 3nt protospacer adajacent motif (PAM) consisting of the sequence 'NGG'.  When designing a gRNA a researcher should aim to maximize target DNA binding and minimize off target effects.  This tool accepts a target DNA sequence and an optional reference sequence and returns a list of suitable gRNA sequences to the user.  

### Implementation
The best gRNA sequence is one that is compatible with the user's cloning strategy, provides maximum target DNA binding, and minimizes off target effects.  These three considerations were evaluated when implementing this tool, and the flow of gRNA design in this tool is as follows.

#### 1- Selection of gRNAs Based on Proximity to the PAM Sequences
When creating a gene knockout it is desirable to target the 5' region of the CDS, thus the first 25% of the provided target sequence is evaluated.  To find potential gRNA sequences, all 20bp regions immediately upstream of a 'NGG' PAM sequnce in both the forward and reverse complemet of the input target sequence were determined.  Next, the candidate gRNA sequence GC content was evaluated, and if the GC content was between 40 and 80% (known to be the optimal range) a sgRNA class object was created with the gRNA sequence and GC content and this was added to a list.

#### 2- Off Target Binding
The best way to minimize off target effects is to select gRNAs that have minimal homology elsewhere in the genome of the host organism.  Off target binding was evaluated if the user provides an optional reference sequence.  To provide a reference sequence, such a host organism genome, the user must provide the reference sequence in the form of a taxid.  Information about [taxid can be found here](https://www.ncbi.nlm.nih.gov/taxonomy "taxid").  

To evaluate off target gRNA binding, the candidate gRNAs selected in (1) were blasted against the reference sequence, if provided, and the [E scores](https://blast.ncbi.nlm.nih.gov/blast/Blast.cgi?CMD=Web&PAGE_TYPE=BlastDocs&DOC_TYPE=FAQ#expect) of the two most significant hits are returned and added to the sgRNA class object.  

Whether the first or second E score is of more interest to the user depends on the application.  For example, if the input target sequence is a sequence present in the reference sequence than the first E score will be nearly zero and the second E score will represent a hit elsewhere in the sequence.  Thus, in this case the second E score is of more interest to the user.  However, if the target sequence is an exogenous sequence the first E score will be of more interest to the user.

### Example
To design candidate gRNAs againt the Synechococcus elongatus PCC 7942 (taxid = 1140) sequence found in 'example_target.txt' the following is executed in the terminal:

```
$ python3 gRNA.py example_target.txt 1140
```
35 candidate gRNAs were identified, and sample output (sgRNA.txt) for the first three is shown below:

gRNA_1  
aacgtgctggcgatcattct  
gc: 0.5, eScore1: 5.88041e-05, eScore2: 0.371094  



gRNA_2  
gtgctggcgatcattctcgg  
gc: 0.6, eScore1: 5.88041e-05, eScore2: 0.371094  



gRNA_3  
ctggcgatcattctcggtgg  
gc: 0.6, eScore1: 5.88041e-05, eScore2: 0.371094  
