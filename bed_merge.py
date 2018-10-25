#!/usr/bin/env python3
import pandas as pd
import os
import argparse

def MergeInterval(sort_list=None):
    interval = []
    last_start = None
    last_end = None
    count = 0
    if len(sort_list) <= 1:
        return sort_list
    for start,end in sort_list:
        count += 1
        if not last_start:
            last_start = start
            last_end = end
            continue
        if last_end < start: #两个集合没有交集
            out_start = last_start
            out_end = last_end
            interval.append([out_start,out_end])
        else: #两个集合有交集
            start =last_start

        if count == len(sort_list): #如果是最后一个数
            interval.append([start, end])

        last_start = start
        last_end = end
    return interval


def Xopen(bedfile=None):
    out_file = os.path.basename(bedfile) + ".merge"
    df = (pd.read_csv(bedfile,header=None,sep="\t",usecols=[0,1,2],names=["chrom","start","end"])
            .sort_values(by=["chrom","start","end"],ascending=True)
            .astype({"start":'int32',"end":"int32"})
          )
    out_dict = {}
    try:
        oo = open(out_file,"w")
    except TypeError as e:
        print(e)
        exit(1)

    for chrom,start,end in zip(df.chrom,df.start,df.end):
        out_dict[chrom] = out_dict.get(chrom,[])
        out_dict[chrom].append([start,end])
    for chrom in out_dict:
        chrom_merge_bed = MergeInterval(sort_list=out_dict[chrom])
        for start,end in chrom_merge_bed:
            print(chrom,start,end,sep= "\t",file=oo)
    oo.close()

def GetPar():
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--bed", help="bed file at least three columns It is respectively chrom start end",required=True)
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    par = GetPar()
    Xopen(bedfile=par.bed)

# bedfile = "/project/BIT/keke.zou/pycharm/p3/TMB/hot_spot/F1CDx_exon.bed"
# Xopen(bedfile)
#print(MergeInterval(sort_list=[[1,2],[2,3],[5,7],[6,9],[7,12],[14,17]]))
#print(MergeInterval(sort_list=[[1,2],[4,5]]))
