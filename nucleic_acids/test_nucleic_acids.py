import unittest
from nucleic_acids import NucleicAcid, Dna, Rna


class TestNucleicAcid(unittest.TestCase):
    def test_insufficient_args(self):
        self.assertRaises(ValueError, NucleicAcid, 'atucatagatau')  # T and U cannot be found together in nucleic acid
        self.assertRaises(ValueError, NucleicAcid, 'donotcallcthulhu')  # test for random string
        self.assertRaises(ValueError, NucleicAcid, '')  # test for empty string

    def test_types(self):
        self.assertRaises(TypeError, NucleicAcid, True)  # object must be instantiated only with str input, not bool
        self.assertRaises(TypeError, NucleicAcid, 18)  # test for int
        self.assertRaises(TypeError, NucleicAcid, 14.8)  # same test for float
        self.assertRaises(TypeError, NucleicAcid, 1 + 5j)  # same test for complex number

    def test_gc_content(self):  # correctness of GC-content calculation
        test_gc = {'ATGCGCATGTGTCCAT': 0.5,
                   'atgcgcatgtgtccat': 0.5, 'GATTACAT': 0.25, 'TATTAATA': 0, 'GGCCGGCCGGCGCCGGCGCGCGCCGGGCC': 1}
        for seq, gc in test_gc.items():
            sequence = NucleicAcid(seq)
            gc = sequence.gc_content()
            self.assertAlmostEqual(gc, test_gc[seq])


class TestDna(unittest.TestCase):
    def test_insufficient_args(self):  # as for NucleicAcid, but with Dna
        self.assertRaises(ValueError, Dna, 'atucatagatau')
        self.assertRaises(ValueError, Dna, 'uaauagugagcgcaa')
        self.assertRaises(ValueError, Dna, 'intentional_bullshit')
        self.assertRaises(ValueError, Dna, '')

    def test_complement(self):  # correctness of transcription
        test_complement = {'atgcgcatgtgtccat': 'TACGCGTACACAGGTA', 'GATTACAT': 'CTAATGTA',
                           'TATTAATA': 'ATAATTAT', 'GGCCGGCCGGCGCCGGCGCGCGCCGGGCC': 'CCGGCCGGCCGCGGCCGCGCGCGGCCCGG'}
        for seq, complement in test_complement.items():
            sequence = Dna(seq)
            compl = sequence.complement()
            self.assertEqual(compl, test_complement[seq])

    def test_revcomp(self):  # correctness of reverse complement
        test_revcomp = {'atgcgcatgtgtccat': 'ATGGACACATGCGCAT', 'GATTACAT': 'ATGTAATC', 'TATTAATA': 'TATTAATA',
                        'GGCCGGCCGGCGCCGGCGCGCGCCGGGCC': 'GGCCCGGCGCGCGCCGGCGCCGGCCGGCC'}
        for seq, revcomp in test_revcomp.items():
            sequence = Dna(seq)
            revcomp = sequence.reverse_complement()
            self.assertEqual(revcomp, test_revcomp[seq])


class TestRna(unittest.TestCase):
    def test_insufficient_args(self):  # as for NucleicAcid, but with Dna
        self.assertRaises(ValueError, Rna, 'atucatagatau')
        self.assertRaises(ValueError, Rna, 'taatagtgagcgcaa')
        self.assertRaises(ValueError, Rna, 'intentional_bullshit')
        self.assertRaises(ValueError, Rna, '')

    def test_complement(self):
        test_complement = {'agcgcauguguccau': 'UCGCGUACACAGGUA',
                           'GAUUACAU': 'CUAAUGUA',
                           'UAUUAAUA': 'AUAAUUAU',
                           'GGCCGGCCGGCGCCGGCGCGCGCCGGGCC': 'CCGGCCGGCCGCGGCCGCGCGCGGCCCGG'}
        for seq, complement in test_complement.items():
            sequence = Rna(seq)
            compl = sequence.complement()
            self.assertEqual(compl, test_complement[seq])


if __name__ == '__main__':
    unittest.main()
