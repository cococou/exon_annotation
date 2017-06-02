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
          -b bed file,the chr start end must be exist.
          -r refGene.txt , if you have not this file ,this command line "wget http://hgdownload.soe.ucsc.edu/goldenPath/hg19/database/refGene.txt" can be used to get it.
    """,file = sys.stderr)
    exit()

def Defalut_par():
    Pardic = {
         'UCSC' : "NA",
         'BED' : "NA",
    }
    return Pardic

def PAR(argv):
    Pardic = Defalut_par()
    opts, args = getopt.getopt(argv[1:], 'hvr:b:')
    for o, a in opts:
        if o == ('-h'):
            Usage()
        elif o == ('-v'):
            Version()
        elif o == ('-r'):
            Pardic['UCSC'] =  a
        elif o == ('-b'):
            Pardic['BED'] =  a
        else:
            print('unhandled option',file=sys.stderr)
            exit()
    return Pardic

def ERR(string):
    if string == 'NA':
        print('Miss required parameter',file=sys.stderr)
        Usage()
        
def handle_exon(Pardic):
    ERR(Pardic['BED'])
    with open(Pardic['BED']) as f:
        for line in f:
            line = line.strip()
            if not line: continue
            if line.startswith("#"): continue
            l = line.split(None)
            yield l[0],int(l[1]),int(l[2]),line

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
    out = []
    Pardic = PAR(argv)
    exon_file = handle_exon(Pardic)
    for chr,start,end,line in exon_file:
        ref_file = handle_ref(Pardic)
        chr = 'chr'+chr
        for NM,CHR,EXON_start,EXON_end,GENE in ref_file:
            GENE = GENE.upper()
            anno = "";anno_start = '';anno_end = ''
            exon_starts = EXON_start.split(',');exon_ends = EXON_end.split(',')
            exon_starts.pop();exon_ends.pop()
            if CHR==chr and start >= int(exon_starts[0]) and end <= int(exon_ends[len(exon_ends)-1]) :
                anno = GENE
                for i in list(range(0,len(exon_starts))):
                    if start >= int(exon_starts[i]) and start <= int(exon_ends[i]):
                        anno_start = "E."+str(i+1)
                        anno_end = "E."+str(i+1)
                        print("+++",anno_start)
                        print('---',anno_end)
                        break
                    #if anno_end != "" or anno_start != "":
                break
        if anno.upper() in line.upper():
            print(line+":"+anno_start+":"+anno_end)
        else:
            if line.endswith(";"):
                print(line+anno+":"+anno_start+":"+anno_end)
            else:
                print(line,anno,":"+anno_start+":"+anno_end,sep=";")

if __name__ == '__main__':
    main(sys.argv)     
