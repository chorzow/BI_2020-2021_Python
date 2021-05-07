import sys
import os


def help_and_exit():
    print(
        """
Program: FASTQf (FASTQ filtrator)
Version: 2.0
Contacts: Andrey Sobolev (github.com/chorzow)

Usage: python3 filter_fastq2.py [OPTIONS] FASTQ_PATH

    Filter a .fastq file.

    FASTQ_PATH: Path to a FASTQ file.

Options:
    --min_length <int>  Minimal length of the read to pass filtration. Must be a positive integer.
    --keep_filtered     Write filtered reads to separate file.
    --gc_bounds <int> <int> Range of GC content in the read. 1 or 2 values can be provided.
                        One value is treated as a lower threshold; two values are treated as a range of GC content.
                        E.g., --gc_bounds 55 leaves only reads with GC >=55%;
                              --gc_bounds 55 60 leaves only reads with 55 =< GC >= 60
    --output_base_name <str>  Base name to use for output file(s).
    --help          Show this message and exit.
"""
        )
    sys.exit(1)


supported_args = ['--min_length', '--keep_filtered', '--gc_bounds', '--output_base_name']

parsed_args = {
        '--min_length': 0,
        '--keep_filtered': False,
        '--gc_bounds': [],
        '--output_base_name': '',
        'fastq_path': '.'
    }


def parse_min_length(args_lst):
    minlen = 0
    if '--min_length' in args_lst:
        idx = args_lst.index('--min_length')
        try:
            minlen = int(args_lst[idx + 1])
        except ValueError:
            raise ValueError(f'{args_lst[idx + 1]} is not a valid value for --min_length. Type --help for usage.')
        if args_lst[idx + 2].lstrip('-').isdigit():
            raise ValueError('--min_length takes maximum 1 value as input. Type --help for usage.')
        elif int(args_lst[idx + 1]) < 0:
            raise ValueError('--min_length must be a non-negative integer. Type --help for usage.')
    return minlen


def parse_keep_filtered(args_lst):
    if '--keep_filtered' in args_lst:
        keep_filtered = True
    else:
        keep_filtered = False
    return keep_filtered


def parse_gc_bounds(args_lst):
    gc_bounds = [0.0, 0.0]
    if '--gc_bounds' in args_lst:
        idx = args_lst.index('--gc_bounds')

        try:
            gc_bounds = [float(args_lst[idx + 1])]
        except ValueError:
            raise ValueError(f'{args_lst[idx + 1]} is not a valid value for --gc_bounds argument. See --help for more')

        try:
            gc_bounds.append(float(args_lst[idx + 2]))
        except (IndexError, ValueError):
            gc_bounds.append(float(args_lst[idx + 1]))

        try:
            if args_lst[idx + 3].isdigit():
                raise ValueError('--gc_bounds takes maximum 2 values as input. Type --help for usage.')
        except IndexError:
            pass
    for i in gc_bounds:
        if i < 0 < 100:
            raise ValueError('Wrong value: GC content of the sequence varies from 0 to 100.')
        elif i > i + 1:
            raise ValueError('Lower threshold of gc_bounds must be less than the upper one. Type --help for usage.')
    return gc_bounds


def parse_file_name(args_lst):
    path = args_lst[-1]
    file_name = path.split('/')[-1]
    if not os.path.exists(path):
        raise ValueError(f'No such file: {path}.\n'
                         f'Please specify a valid path to a .fastq or .fq file. Type --help for usage.')
    if not file_name.endswith('.fastq') or file_name.endswith('.fq'):
        raise ValueError(f'Wrong format: {path} is not a .fastq or .fq file. Type --help for usage.')
    return file_name, path


def parse_output_base_name(args_lst):
    if '--output_base_name' in args_lst:
        idx = args_lst.index('--output_base_name')
        if idx == len(args_lst) - 1 or idx + 1 == len(args_lst) - 1 or args_lst[idx + 1] in supported_args:
            raise ValueError('Please specify a valid output base name. Type --help for usage.')
        try:
            output_name = args_lst[idx + 1]
        except (ValueError, IndexError):
            raise ValueError('Please specify a valid output base name. Type --help for usage.')

    else:
        file_name, path = parse_file_name(args_lst)
        output_name, _ = file_name.split('.fastq')
    return output_name


def parse_args(args_lst):
    if '--help' in args_lst:
        help_and_exit()
    for i in args_lst:
        if i.startswith('--') and i not in supported_args:
            raise ValueError(f'{i} is not a valid argument. See --help for available options.')
    parsed_args['--min_length'] = parse_min_length(args_lst)
    parsed_args['--keep_filtered'] = parse_keep_filtered(args_lst)
    parsed_args['--gc_bounds'] = parse_gc_bounds(args_lst)
    _, parsed_args['fastq_path'] = parse_file_name(args_lst)
    parsed_args['--output_base_name'] = parse_output_base_name(args_lst)

    return parsed_args


def gc_count(read):
    read = read.upper().strip()
    return (read.count('C') + read.count('G')) * 100 / len(read)


def valid_len(read, minlen):
    if len(read.upper().strip()) < minlen:
        return False
    else:
        return True


def valid_gc(read, gc_bounds):
    if gc_bounds[0] == gc_bounds[1]:
        if gc_count(read) < gc_bounds[0]:
            return False
    elif gc_bounds[0] < gc_bounds[1]:
        if gc_count(read) < gc_bounds[0] or gc_count(read) > gc_bounds[1]:
            return False
    return True


def file_exists(output_base_name):
    suffices = ['passed', 'failed']
    for suffix in suffices:
        if os.path.exists(f'{output_base_name}__{suffix}.fastq'):
            ans = input(f'File {output_base_name}__{suffix}.fastq already exists. Overwrite? [y/n]')
            if ans == 'y':
                os.remove(f'{output_base_name}__{suffix}.fastq')
            elif ans == 'n':
                print('Aborted.')
                sys.exit(1)
            else:
                raise ValueError('Aborted. Please try again and type y or n.')


def write_to_file(parsed_args):
    minlen = parsed_args['--min_length']
    keep_filtered = parsed_args['--keep_filtered']
    gc_bounds = parsed_args['--gc_bounds']
    output_base_name = parsed_args['--output_base_name']
    fastq_path = parsed_args['fastq_path']
    output_passed = output_base_name + '__passed.fastq'
    file_exists(output_base_name)

    with open(fastq_path, 'r') as inf:
        read = []
        passed = 0
        failed = 0

        for line in inf:
            if len(read) != 3:
                read.append(line.strip())
                continue
            else:
                read.append(line.rstrip())
                with open(output_passed, 'a') as ouf_passed:
                    if valid_gc(read[1], gc_bounds) and valid_len(read[1], minlen):
                        ouf_passed.write('\n'.join(read) + '\n')
                        passed += 1
                    else:
                        if keep_filtered:
                            output_failed = output_base_name + '__failed.fastq'
                            with open(output_failed, 'a') as ouf_failed:
                                ouf_failed.write('\n'.join(read) + '\n')
                        failed += 1

            read = []
    return passed, failed


if __name__ == '__main__':
    parsed_args = parse_args(sys.argv[1:])
    passed, failed = write_to_file(parsed_args)
    print('Filtering finished.')
    print(f'Total reads in {parsed_args["fastq_path"]}: {passed + failed}, of them:\n'
          f'{passed} ({round(passed * 100 / (passed + failed), 2)}%) passed.\n'
          f'{failed} ({round(failed * 100 / (passed + failed), 2)}%) failed.')




