import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from Bio import SeqIO

#--------1. Line plot--------
x = np.arange(1, 23, 2)
y = np.arange(20, 42, 2)

plt.xticks(x)
plt.yticks(y)
plt.xlim(1, 21)
plt.ylim(20,40)
plt.plot(x, y)

plt.xlabel('Odd numbers')
plt.ylabel('Even numbers')
plt.title('1. Line plot')
plt.savefig('lineplot.png')

#--------2. Sequence length distribution--------

def seq_length_distribution(path):
    sizes = [len(rec) for rec in SeqIO.parse(path, 'fasta')]
    plt.hist(sizes, edgecolor='black')
    plt.title("%i sequences\nLengths %i to %i" % (len(sizes), min(sizes), max(sizes)))
    plt.xlabel('Sequence length (bp)')
    plt.ylabel('Count')
    plt.savefig(path + '.png')

seq_length_distribution('example.fasta')

#--------3. My favourite plot--------

plot_data = np.random.rand(10, 12)
ax = sns.heatmap(plot_data)
plt.title('My favourite plot is heatmap!')
plt.savefig('heatmap.png')
