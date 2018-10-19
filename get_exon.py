#!/usr/bin/env python3
import os
import sys
import pandas as pd
import numpy as np

def get_target(f):
    target = []
    with  open(f) as ff:
        for line in ff:
            line = line.strip()
            if line.startswith("#"): continue
            l = line.split("\t")
            if not l:continue
            target.append(l[0])
    return target

def xopen_p(ref_file):
    df = pd.read_csv(ref_file,compression="gzip",header=None,sep="\t",usecols=[1,2,3,9,10,12])
    df.columns = ['NMID',"CHROM","ORI","ST","ED","GENE"]
    return df

def ssp(xx):
    sts= xx.ST.split(",")[:-1]
    eds = xx.ED.split(",")[:-1]
    df = (pd.DataFrame({"ED":eds,"ST":sts})
            .assign(NMID = np.array(xx.NMID))
            .assign(CHROM=np.array(xx.CHROM))
            .assign(ORI=np.array(xx.ORI))
            .assign(GENE=np.array(xx.GENE))
          )
    return df

def main(NM_ID=None,ref_file=None):
    ID = get_target(NM_ID)
    df = xopen_p(ref_file).query("NMID in @ID")
    #df = df.apply(ssp,axis =1)
    for i in range(0,df.shape[0]):
        if i == 0:
            dff = ssp(df.iloc[i])
        else:
            dff = pd.concat([ssp(df.iloc[i]),dff],)
    dff.to_csv(os.path.basename(NM_ID)+".anno",sep="\t",columns=['CHROM',"ST","ED","NMID","GENE","ORI"],header=None,index=None)

if __name__ == "__main__":
    try:
        NM_ID,ref_file = sys.argv[1:]
    except:
        print("python3 script [NM_ID list file] [refGene.txt.gz]")
        exit()
    main(NM_ID=NM_ID,ref_file=ref_file)
# f = "NM_ID.txt"
# ref_file = "/soft/humandb/UCSC/refGene.txt.gz"
# main(NM_ID=f,ref_file=ref_file)
