import unittest
from filter_fastq2 import *


class TestFilterFastq2(unittest.TestCase):
    def setUp(self):
        self.arg_lst_full = ['filter_fastq2.py', '--min_length', '60', '--gc_bounds', '55', '60', '--keep_filtered',
                             '--output_base_name', 'filtered', 'test.fastq']  # full correct input
        self.parsed_args_full = {
            '--min_length': 60,
            '--keep_filtered': True,
            '--gc_bounds': [55.0, 60.0],
            '--output_base_name': 'filtered',
            'fastq_path': 'test.fastq'
        }
        self.parsed_args_no_opt = {
            '--min_length': 0,
            '--keep_filtered': False,
            '--gc_bounds': [0.0, 0.0],
            '--output_base_name': 'test',
            'fastq_path': 'test.fastq'
        }
        self.read1 = ['@test_read1\n',
                      'CCCCCGGCGGCCGGGGCCGGCCGGGCCCGGGGGGCCCCCCCGGGGGCCCCCCCGGCGGCGGCGCGGGGGGGCCCGCGGGGGGGGGGGGGGGGG\n',
                      '+\n',
                      'CCCFFFFFHHHHHJJJJJJJJJJFFHIJJJJJJJJJJJJJJJJIJHHHHHHFDEDF;AEEEEEEDDDDDBBACDDDCDDDDCCDDDDDDCCDC\n']
        self.read2 = ['@test_read2\n',
                      'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n',
                      '+\n',
                      'CCCFFFFFHHHHHJHIIJIIIIJJJJJJGIIJJIIGHJJJJJIIJJDHEDFFACDDDCDDDDCCDDECACCDCCCDACDDDDCCDDDDDBD@A\n']
        self.read3 = ['@test_read3\n', 'GTGACGTTAG\n', '+\n', 'BD;:=:?@\n']
        # --------parse_minlen--------
        self.arg_lst_minlen = ['filter_fastq2.py', '--min_length', '60', 'test.fastq']
        self.arg_lst_minlen_neg = ['filter_fastq2.py', '--min_length', '-2', 'test.fastq']  # negative value
        self.arg_lst_minlen_float = ['filter_fastq2.py', '--min_length', '25.54', 'test.fastq']  # float
        self.arg_lst_minlen_str = ['filter_fastq2.py', '--min_length', 'samplestring', 'test.fastq']  # string
        self.arg_lst_minlen_two = ['filter_fastq2.py', '--min_length', '60', '80' 'test.fastq']  # two values
        self.arg_lst_no_minlen = ['filter_fastq2.py', '--min_length', 'test.fastq']  # invalid value for min_length
        # --------parse_gc_bounds--------
        self.arg_lst_gc_str = ['filter_fastq2.py', '--gc_bounds', 'qwe', 'rty',
                               'test.fastq']  # invalid value(s) for gc_bounds
        self.arg_lst_gc3 = ['filter_fastq2.py', '--gc_bounds', '55', '65', '75',
                            'test.fastq']  # too many values for gc_bounds
        self.arg_lst_gc1 = ['filter_fastq2.py', '--gc_bounds', '30', 'test.fastq']  # one value for gc_bounds
        self.arg_lst_gc0 = ['filter_fastq2.py', '--gc_bounds', 'test.fastq']  # no values for gc_bounds
        self.arg_lst_gc_neg = ['filter_fastq2.py', '--gc_bounds', '-10', 'test.fastq']  # negative GC content
        self.arg_lst_gc_pos = ['filter_fastq2.py', '--gc_bounds', '112', 'test.fastq']  # GC content over 100%
        self.arg_lst_gc_less = ['filter_fastq2.py', '--gc_bounds', '50', '30', 'test.fastq']
        # --------parse_output_base_name--------
        self.arg_lst_no_opt = ['filter_fastq2.py', 'test.fastq']  # no optional arguments
        self.arg_lst_no_base1 = ['filter_fastq2.py', '--output_base_name',
                                 'test.fastq']  # no output_base_name specified
        self.arg_lst_no_base2 = ['filter_fastq2.py', '--output_base_name', '--keep_filtered', 'test.fastq']
        self.arg_lst_no_base3 = ['filter_fastq2.py', '--output_base_name']
        # --------parse_file_name--------
        self.arg_lst_abs_path = ['filter_fastq2.py', '/home/chorzow/BI/Python/fastq-filtrator/test.fastq']
        self.arg_lst_faq = ['filter_fastq2.py', '--min_length', '60', '--gc_bounds', '55', '60', '--keep_filtered',
                            '--output_base_name', 'filtered', 'test.faq']  # wrong file extension
        self.arg_lst_no_file = ['filter_fastq2.py', '/home/chorzow/BI/Python/fastq-filtrator/my_fancy_fastq.fastq']
        # --------parse_args--------
        self.arg_lst_typo = ['filter_fastq2.py', '--min_lenghh', '60', '--gc_bounds', '55', '60',
                             'test.fastq']  # typo in arguments
        # --------valid_minlen--------
        self.minlen = 30
        # --------valid_gc--------
        self.gc_bounds1 = [0.0, 0.0]
        self.gc_bounds2 = [50.0, 50.0]
        self.gc_bounds3 = [30.0, 50.0]

    def test_parse_min_length(self):
        self.assertEqual(parse_min_length(self.arg_lst_minlen), 60)
        with self.assertRaises(ValueError):
            parse_min_length(self.arg_lst_minlen_neg)
            parse_min_length(self.arg_lst_minlen_float)
            parse_min_length(self.arg_lst_minlen_str)
            parse_min_length(self.arg_lst_minlen_two)
            parse_min_length(self.arg_lst_no_minlen)

    def test_parse_keep_filtered(self):
        self.assertEqual(parse_keep_filtered(['filter_fastq2.py', '--keep_filtered', 'test.fastq']), True)
        self.assertEqual(parse_keep_filtered(['filter_fastq2.py', 'test.fastq']), False)

    def test_parse_gc_bounds(self):
        self.assertEqual(parse_gc_bounds(self.arg_lst_full), [55.0, 60.0])
        self.assertEqual(parse_gc_bounds(self.arg_lst_gc1), [30.0, 30.0])
        self.assertEqual(parse_gc_bounds(self.arg_lst_no_opt), [0.0, 0.0])
        with self.assertRaises(ValueError):
            parse_gc_bounds(self.arg_lst_gc0)
            parse_gc_bounds(self.arg_lst_gc3)
            parse_gc_bounds(self.arg_lst_gc_str)
            parse_gc_bounds(self.arg_lst_gc_neg)
            parse_gc_bounds(self.arg_lst_gc_pos)
            parse_gc_bounds(self.arg_lst_gc_less)

    def test_parse_output_base_name(self):
        self.assertEqual(parse_output_base_name(self.arg_lst_full), 'filtered')
        self.assertEqual(parse_output_base_name(self.arg_lst_no_opt), 'test')
        with self.assertRaises(ValueError):
            parse_output_base_name(self.arg_lst_no_base1)
            parse_output_base_name(self.arg_lst_no_base2)
            parse_output_base_name(self.arg_lst_no_base3)

    def test_parse_file_name(self):
        self.assertEqual(parse_file_name(self.arg_lst_full), ('test.fastq', 'test.fastq'))
        self.assertEqual(parse_file_name(self.arg_lst_abs_path),
                         ('test.fastq', '/home/chorzow/BI/Python/fastq-filtrator/test.fastq'))
        with self.assertRaises(ValueError):
            parse_file_name(self.arg_lst_no_file)
            parse_file_name(self.arg_lst_faq)

    def test_parse_args(self):
        self.assertEqual(parse_args(self.arg_lst_full), self.parsed_args_full)
        self.assertEqual(parse_args(self.arg_lst_no_opt), self.parsed_args_no_opt)
        with self.assertRaises(ValueError):
            parse_args(self.arg_lst_typo)

    def test_gc_count(self):
        self.assertEqual(gc_count(self.read1[1]), 100.0)
        self.assertEqual(gc_count(self.read2[1]), 0.0)
        self.assertEqual(gc_count(self.read3[1]), 50.0)

    def test_valid_len(self):
        self.assertEqual(valid_len(self.read1[1], self.minlen), True)
        self.assertEqual(valid_len(self.read2[1], self.minlen), True)
        self.assertEqual(valid_len(self.read3[1], self.minlen), False)

    def test_valid_gc(self):
        self.assertEqual((valid_gc(self.read1[1], self.gc_bounds1),
                          valid_gc(self.read2[1], self.gc_bounds1),
                          valid_gc(self.read3[1], self.gc_bounds1)), (True, True, True))
        self.assertEqual((valid_gc(self.read1[1], self.gc_bounds2),
                          valid_gc(self.read2[1], self.gc_bounds2),
                          valid_gc(self.read3[1], self.gc_bounds2)), (True, False, True))
        self.assertEqual((valid_gc(self.read1[1], self.gc_bounds3),
                          valid_gc(self.read2[1], self.gc_bounds3),
                          valid_gc(self.read3[1], self.gc_bounds3)), (False, False, True))

    def test_write_to_file(self):
        self.assertEqual(write_to_file(self.parsed_args_full), (2, 23))
        with open('filtered__passed.fastq', 'r') as inf:
            filtered_passed = len(inf.readlines())
        with open('filtered__failed.fastq', 'r') as inf:
            filtered_failed = len(inf.readlines())
        self.assertEqual(filtered_passed, 2 * 4)
        self.assertEqual(filtered_failed, 23 * 4)
        self.assertEqual(write_to_file(self.parsed_args_no_opt), (25, 0))
        with open('test__passed.fastq', 'r') as inf:
            test_passed = len(inf.readlines())
        self.assertEqual(test_passed, 25 * 4)


if __name__ == '__main__':
    unittest.main()
