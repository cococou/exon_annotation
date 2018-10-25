## exon file
get annotated exon file from ucsc
download website: http://hgdownload.soe.ucsc.edu/goldenPath/hg19/database/refGene.txt

## get exon region
by given gene list or NMID to get every exon and its position

```sh
python3 get_exon.py -h
```

## merge exon region
merge all exon region to make sure all regions are unique

```sh
python3 bed_merge.py -h
```
 


