import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
from collections import defaultdict, Counter

path = "datasets/bitly_usagov/example.txt"
records = [json.loads(line) for line in open(path)]

time_zones = [rec['tz'] for rec in records if 'tz' in rec]

def get_counts1(sequence):
    counts = {}
    for i in sequence:
        if i in counts:
            counts[i] += 1
        else:
            counts[i] = 1
    return counts

def get_counts2(sequence):
    counts = defaultdict(int)
    for i in sequence:
        counts[i] += 1
    return counts

def top_counts1(count_dict, n = 10):
    counts = get_counts1(count_dict)
    pairs = [(tz, i) for tz, i in counts.items()]
    return pairs[:n]

def top_counts2(count_dict, n = 10):
    counts = Counter(count_dict)
    pairs = counts.most_common(n)
    return pairs

tz_count = get_counts1(time_zones)
top_10 = top_counts1(time_zones)
print(tz_count['America/New_York'])
print(top_10)

#using pandas
frame = pd.DataFrame(records)
time_zones_pd = frame['tz'].value_counts()
print(time_zones_pd[:10])

subset = time_zones_pd[:10]
sns.barplot(y = subset.index, x = subset.values)

result = pd.Series([a.split()[0] for a in frame.a.dropna()])
browser_count = result.value_counts()
print(browser_count[:10])

cframe = frame[frame.a.notnull()]
cframe['os'] = np.where(cframe.a.str.contains('Windows'), 'Windows', 'Not Windows')
os_count = cframe['os'].value_counts()
print(os_count)

by_tz_os = cframe.groupby(['tz', 'os'])
agg_counts = by_tz_os.size().unstack().fillna(0)
print(agg_counts.head())

indexer = agg_counts.sum(1).argsort()
print(indexer.head())

count_subset = agg_counts.take(indexer[-10:])
count_subset = count_subset.stack()
count_subset.name = 'total'
count_subset = count_subset.reset_index()
print(count_subset[:10])
sns.barplot(data=count_subset, y='tz', x='total', hue='os')

def norm_total(group):
    group['normed_total'] = group.total / group.total.sum()
    return group

results = count_subset.groupby('tz').apply(norm_total)

sns.barplot(x='normed_total', y='tz', hue='os', data=results)




