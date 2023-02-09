README

1. Isabella's clustering step (results in clustered FASTA file--we used 95% threshold for this one)

2. Run BLAST on the FASTA file from step 1. This is the job script that we use to do it (to run, use "sbatch <jobfilename.job> <fastafilename>":


#!/bin/bash

#SBATCH --time=72:00:00   # walltime
#SBATCH --ntasks=18   # number of processor cores (i.e. tasks)
#SBATCH --nodes=1   # number of nodes
#SBATCH --mem-per-cpu=4096M   # memory per CPU core
#SBATCH -J "invert_blast"   # job name
#SBATCH --mail-user=paul_frandsen@byu.edu   # email address
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL


# Set the max number of threads to use for programs using OpenMP. Should be <= ppn. Does nothing if the program doesn't use OpenMP.
export OMP_NUM_THREADS=$SLURM_CPUS_ON_NODE

# LOAD MODULES, INSERT CODE, AND RUN YOUR PROGRAMS HERE
module purge
source ~/.bashrc
conda activate blast
blastn -query $1 -db /apps/blast/databases/nt -outfmt "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore staxids" -max_target_seqs 10 -max_hsps 1 -evalue 1e-25 -num_threads $SLURM_NPROCS > `basename $1 fasta`blastout


3. Extract the best hit from each sequence with pick_best_seq.py. This script basically goes through all of the sequences and chooses the one with the longest length and best e-values. You can run it on the *blastout file with:

python pick_best_seq.py file.blastout best_blast_hits.txt

4. Use taxonkit to download the lineages for the taxa that we recovered with BLAST (this is assuming you've already installed taxonkit via conda)

conda activate taxonkit
taxonkit lineage -i 2 best_blast_hits.txt | taxonkit reformat -I 2 > best_lineage.txt

5. Use the python script reformat_lineage.py to reformat the output file for input into qiime2

python reformat_lineage.py best_lineage.txt best_lineage_reformatted.txt