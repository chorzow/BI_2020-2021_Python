class NucleicAcid:
    def __init__(self, seq):
        alphabet = {'A', 'C', 'T', 'G', 'U'}
        self.seq = seq
        if type(self.seq) is not str:
            raise TypeError(f'{self.seq} is not a nucleic acid sequence.')
        if self.seq == '':
            raise ValueError('Please specify a non-empty sequence.')
        self.seq = seq.upper()
        self.index = 0
        for i in self.seq:
            if 'T' in self.seq and 'U' in self.seq:
                raise ValueError('Wrong sequence: T and U cannot be found together in a nucleic acid sequence.')
            if i not in alphabet:
                raise ValueError(self.seq + ' is not a nucleic acid sequence.')

    def __len__(self):
        return len(self.seq)

    def __iter__(self):
        return self

    def __next__(self):
        try:
            result = self.seq[self.index]
        except IndexError:
            raise StopIteration
        self.index += 1
        return result

    def gc_content(self):
        """Count GC-content of the sequence"""
        gc = 0
        for i in self.seq:
            if i == 'G' or i == 'C':
                gc += 1
        # return f"Sequence {self.seq}: GC content {round(gc / len(self) * 100, 2)}%"
        return round(gc / len(self), 2)


class Dna(NucleicAcid):
    """A DNA sequence."""
    def __init__(self, seq):
        super().__init__(seq)
        for i in self.seq:
            if i not in {'A', 'C', 'T', 'G'}:
                raise ValueError(self.seq + ' is not a DNA sequence.')

    def complement(self):
        """Returns the complementary DNA sequence"""
        chargaff = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
        bases = list(self.seq)
        comp = [chargaff.get(base, base) for base in bases]
        return ''.join(comp)

    def reverse_complement(self):
        """Returns the reverse complement of given DNA sequence."""
        revcomp = reversed(self.complement())
        return ''.join(revcomp)

    def transcribe(self):
        """Returns a RNA sequence corresponding to the given DNA sequence."""
        chargaff = {'A': 'U', 'T': 'A', 'G': 'C', 'C': 'G'}
        bases = list(self.seq)
        trscr = [chargaff.get(base, base) for base in bases]
        transcribed = ''.join(trscr)
        return Rna(transcribed)


class Rna(NucleicAcid):
    """Creates a RNA sequence object."""
    def __init__(self, seq):
        super().__init__(seq)
        for i in self.seq:
            if i not in {'A', 'U', 'G', 'C'}:
                raise ValueError(self.seq + ' is not a RNA sequence.')

    def complement(self):
        """Returns the complementary RNA sequence."""
        chargaff = {'A': 'U', 'U': 'A', 'G': 'C', 'C': 'G'}
        bases = list(self.seq)
        comp = [chargaff.get(base, base) for base in bases]
        return ''.join(comp)

