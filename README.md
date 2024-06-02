# MDU.Research.Project
![Banksia serrata painted by Hilary Ash](/assets/images/IMG_0822)
A genomic framework for enhanced strain identification: to improve outbreak detection and public health surveillance using Enterobacter Cloacae Complex 
as an exemplar.

Supervisor: Dr Jake Lacey, Dr Kristy Horen, Prof Benjamin Howden

Student: Susan Noonan

University of Melbourne

Peter Doherty Institute for Infection & Immunity

Master of Science - Bioinformatics

## Research Project

Enterobacter genomes were downloaded and analysed to:
- differentiate the species boundaries
- investigate MLST profiles within species groups
- complete pan-genome analysis
- determine AMR gene profiles

### Quality assessment
[seqkit Github](https://bioinf.shenwei.me/seqkit/)

```Linux
seqkit stat *.fa -a > /path/to_folder/seqkit_stats.txt
```

### Generating MLST profiles and STs
[mlst Github](https://github.com/tseemann/mlst)

```Linux
for f in *.fa do; do mlst --scheme ecloacae $f >> mlst.tsv; done
```
