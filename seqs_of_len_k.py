from itertools import combinations_with_replacement, chain


def generate(k):
    ans = []
    i = 1
    while i < k + 1:
        combs_of_i = list(combinations_with_replacement(['A', 'T', 'G', 'C'], i))
        ans.append(list(''.join(comb) for comb in combs_of_i))
        i += 1
    return chain(*ans)

# Example: print(list(generate(3)))
