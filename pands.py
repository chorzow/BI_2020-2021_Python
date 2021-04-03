#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import missingno as mno
from pandas.plotting import scatter_matrix


# Task 1
train = pd.read_csv('./train.csv')
train.head(10)
train.isna().sum()
# looks like there are some NA values. For the sake of nice plot, they will be set to zero
train = train.fillna(0)
plot_data = train.iloc[:, [0, 6, 7, 8, 9]]  # select necessary columns
plot_data = plot_data.set_index('pos')  # assign first column as indexes

stacked_100 = plot_data.apply(lambda x: x * 100 / sum(x), axis=1)  # convert to absolute fractions - easier to interpret
stacked_100.plot(kind='bar', stacked=True, figsize=(16, 6))

plt.title('Nucleotide fractions by position in sequence')
plt.xlabel('Position in sequence')
plt.ylabel('Nucleotide fraction')
plt.show()


# --------TASK 2--------
train_part = train.loc[train['matches']>train['matches'].mean(), ['pos', 'reads_all', 'mismatches', 'deletions', 'insertions']]
train_part.to_csv('/home/chorzow/BI/Python/pd_hw/train_part.csv')


# --------TASK 3--------
titanic = pd.read_csv('https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv')
titanic.head(10)

# are there any NA values?
titanic.isna().sum()

# Yes, there are. Let's visualize them:
titanic.isna().sum().plot(kind='bar')
plt.show()

# another cool way to do it is using missingno
mno.matrix(titanic)
plt.show()  # a lot of NAs in Age and Cabin. Two in Embarked. They can be clearly visible. Thanks, missingno!

# visualize distributions
pd.plotting.scatter_matrix(titanic.iloc[:, 1:], alpha=0.2, figsize=(12, 12), diagonal='kde')
plt.show()

# "plot" correlations as a background of the correlation dataframe
corr = titanic.corr()
corr.style.background_gradient(cmap='coolwarm')
# another way to visualize correlations (this time as a true plot) is via sns
sns.heatmap(corr,
            xticklabels=corr.columns.values,
            yticklabels=corr.columns.values, cmap='RdYlBu_r')
plt.show()
