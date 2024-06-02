# MDU.Research.Project
![Banksia serrata painted by Hilary Ash](/assets/images/IMG_0822)
A genomic framework for enhanced strain identification: to improve outbreak detection and public health surveillance using Enterobacter Cloacae Complex 
as an exemplar.

Supervisor: Dr Jake Lacey, Dr Kristy Horen, Prof Benjamin Howden

Student: Susan Noonan

University of Melbourne

Peter Doherty Institute for Infection & Immunity

Master of Science - Bioinformatics

Research Project

Enterobacter genomes were downloaded and analysed to differntiate the species boundaries, investigate MLST profiles within species groups, complete pan-genome analysis and determine AMR gene profiles.

### Quality assessment

```Linux
seqkit stat *.fa -a > /path/to_folder/seqkit_stats.txt
```

### Generating MLST profiles and STs

```Linux
for f in *.fa do; do mlst --scheme ecloacae $f >> mlst.tsv; done
```
