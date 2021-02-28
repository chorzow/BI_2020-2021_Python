from Bio import SeqIO


def translate_seq(path, codon_table='Standard'):
    sequences = SeqIO.parse(path, 'fasta')
    for sequence in sequences:
        yield sequence.translate(table=codon_table).seq

transltd = translate_seq('/home/chorzow/BI/Python/functional/ls_orchid.fasta')
print(next(transltd))  # repeat this line to yield new translated sequences from fasta