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

### Pairwise comparisons using SKA
[SKA Github](https://github.com/simonrharris/SKA)
Produce .skf from each fasta file held in a folder called samples.
Move all .skf files to another folder and run ska distance.

```Linux
for i in $(cat isolate_names.txt); do ska fasta *samples/$i -o ska_$i; done
mkdir /ska_folder
mv *.skf /ska_folder
ska distance -s 20 -i 0.9 *.skf -o ska
```

### Mash and Mashtree
[Mash](https://github.com/marbl/Mash)
[Mashtree](https://github.com/lskatz/mashtree)
Produce mash sketch for each isolate.  Make a text file of all .msh files. Move all .msh files into a new folder and run mashtee.

```Linux
for i in $(cat isolate_names.txt); do mash sketch -m 2 *samples/$i; done
mkdir mash_folder
mv *.msh > mash_folder
ls *.msh > mash_list.txt
mash triangle -l mash_list.txt > mash_dist.tab
mashtree *.msh > mash.dnd
```

### Whole genome annotation using Prokka
[Prokka](https://github.com/tseemann/prokka)
Remove the .fa from each sample in the isolate name list. Run prokka on all samples.

```Linux
sed 's/\.fa$//' isolate_names.txt > prokka_names.txt
for f in $(cat prokka_names.txt); do prokka --outdir $f --prefix $f $f.fa --genus Enterobacteriaceae; done
```

### Pan-genome analysis using Panaroo
Add .gff to end of each isolate name used by Prokka. Run panaroo on all the samples.

```Linux
sed 's/$/.gff/' prokka_names.txt > gff_names.txt
mkdir results
panaroo -i gff_names.txt -o /results --clean-mode strict --threads 20
```

### Antimicrobial resistance gene assessment with AbritAMR
[AbritAMR](https://github.com/MDU-PHL/abritamr)
Using a tab separated file called name_path.tab (that contains the isolate name and path_to_that_file), run AbritAMR

```Linux
abritamr run -c name_path.tab -j 16
```

### Use Twilight R scrip to further analyse pan-genome and determine lineage specific markers
[Twilight](https://github.com/twilight-rs/twilight)

```Linux
/path_to/twilight_script.R -p /path_to/panaroo_gene_presence_absence.Rtab -g /path_to/traits_file.tsv -s 5
```
