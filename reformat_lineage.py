import sys

infilename = sys.argv[1]
outfilename = sys.argv[2]

with open(infilename) as infile:
    with open(outfilename, "w") as outfile:
        for line in infile:
            new_line = line.split("\t")
            taxon = new_line[0]
            classification = new_line[3].split(";")
            lineage = ["k_" + classification[0], "p_" + classification[1], "c_" + classification[2], 
                       "o_" + classification[3], "f_" + classification[4], "g_" + classification[5], 
                       "s_" + classification[6]]
            outfile.write(taxon + "\t" + ";".join(lineage) + "\n")