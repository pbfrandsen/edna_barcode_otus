import sys

infilename = sys.argv[1]
outfilename = sys.argv[2]

qseq = ''
evalue = 1000
length = 0
taxid = ''

best_seqs = {}

with open(infilename) as infile:
    for i,line in enumerate(infile):
        new_line = line.split("\t")
        if i == 0:
            qseq = new_line[0]
            taxid = new_line[12]
            if ";" in taxid:
                taxid = taxid.split(";")[0] + "\n"
            length = new_line[3]
        else:
            if new_line[0] == qseq:
                if float(new_line[10]) < float(evalue):
                    print("ha")
                    taxid = new_line[12]
                    if ";" in taxid:
                        taxid = taxid.split(";")[0] + "\n"
                    length = new_line[3]
                elif new_line[10] == evalue:
                    # print("ha")
                    if int(new_line[3]) > int(length):
                        taxid = new_line[12]
                        if ";" in taxid:
                            taxid = taxid.split(";")[0] + "\n"
                        length = new_line[3]
            else:
                best_seqs[qseq] = taxid
                qseq = new_line[0]
                evalue = new_line[10]
                taxid = new_line[12]
                length = new_line[3]
        best_seqs[qseq] = taxid

with open(outfilename, "w") as outfile:
    for record in best_seqs:
        outfile.write(record + "\t" + best_seqs[record])
