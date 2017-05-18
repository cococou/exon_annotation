#!/usr/bin/env python3
import re
import sys
import os
import getopt
import json

def Version():
    print("     ====verison is V1.0, write by kkzou=====")
    exit()

def Usage():
    print("""
          -e gene and exon file,the gene name must exist.
          -r refGene.txt , if you have not this file ,this command line "wget http://hgdownload.soe.ucsc.edu/goldenPath/hg19/database/refGene.txt" can be used to get it.
    """,file = sys.stderr)
    exit()

def Defalut_par():
    Pardic = {
         'UCSC' : "NA",
         'EXON' : "NA"
    }
    return Pardic

def PAR(argv):
    Pardic = Defalut_par()
    opts, args = getopt.getopt(argv[1:], 'hvr:e:')
    for o, a in opts:
        if o == ('-h'):
            Usage()
        elif o == ('-v'):
            Version()
        elif o == ('-r'):
            Pardic['UCSC'] =  a
        elif o == ('-e'):
            Pardic['EXON'] = a
        else:
            print('unhandled option',file=sys.stderr)
            exit()
    return Pardic

def ERR(string):
    if string == 'NA':
        print('Miss required parameter',file=sys.stderr)
        Usage()
 

def handle_exon(Pardic):
    ERR(Pardic['EXON'])
    with open(Pardic['EXON']) as f:
        for line in f:
            line = line.strip()
            if not line: continue
            if line.startswith("#"): continue
            l = line.split(None)
            if len(l) > 2:
                exon = ','.join(l[1:])
                yield l[0],exon
            elif len(l) == 2:
                yield l
            else:
                yield l[0],'NA'

def handle_ref(Pardic):
    ERR(Pardic['UCSC'])
    with open(Pardic['UCSC']) as f:
        for line in f:
            line = line.strip()
            if not line: continue
            if line.startswith("#"): continue
            l = line.split(None)
            if not l[1].startswith("NM"): continue
            NM = l[1];CHR = l[2];EXON_start=l[9];EXON_end=l[10];GENE=l[12]
            yield [i.strip() for i in [NM,CHR,EXON_start,EXON_end,GENE]]

def main(argv):
    Pardic = PAR(argv)
    exon_file = handle_exon(Pardic)
    for gene,exon in exon_file:
        gene = gene.upper()
        exons = [] 
        if exon != 'NA':
            exons = [int(i)-1 for i in exon.split(',')]
        ref_file = handle_ref(Pardic)
        for NM,CHR,EXON_start,EXON_end,GENE in ref_file:
            GENE = GENE.upper()
            exon_starts = EXON_start.split(',');exon_ends = EXON_end.split(',')
            exon_starts.pop();exon_ends.pop()
            if GENE == gene:
                if exons:
                    for ie in exons:
                        if ie > len(exon_starts): break
                        #print(CHR.replace("chr",""),str(int(exon_starts[ie])-10),str(int(exon_ends[ie])+10),GENE+'.E'+str(ie+1),sep = "\t")
                        print(CHR.replace("chr",""),exon_starts[ie],exon_ends[ie],GENE+'.E'+str(ie+1),sep = "\t")
                else:
                    for iE in list(range(0,len(exon_starts))): 
                        #print(CHR.replace("chr",""),str(int(exon_starts[iE])-10),str(int(exon_ends[iE])+10),GENE+'.E'+str(iE+1),sep = "\t")        
                        print(CHR.replace("chr",""),exon_starts[iE],exon_ends[iE],GENE+'.E'+str(iE+1),sep = "\t")

if __name__ == '__main__':
    main(sys.argv)     
