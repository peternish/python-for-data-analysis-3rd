import numpy as np
import pandas as pd
import seaborn as sns

years = range(1880, 2011)
columns = ['name', 'gender', 'number']

baby_data = []
for year in years:
    frame = pd.read_table('datasets/babynames/yob{}.txt'.format(year), sep=',', names=columns)
    frame['year'] = year
    baby_data.append(frame)
baby_data = pd.concat(baby_data, ignore_index=True)

total_birth = baby_data.pivot_table('number', index='year', columns='gender', aggfunc='sum')
total_birth.plot(title = 'male and female birth along the year')

def prop(group):
    group['prop'] = group.number/group.number.sum()
    return group

names = baby_data.groupby(['year','gender']).apply(prop)

def get_top1000(group):
    return group.sort_values(by='number', ascending=False)[:1000]

grouped = names.groupby(['year', 'gender'])
top1000 = grouped.apply(get_top1000)
# Drop the group index, not needed
top1000.reset_index(inplace=True, drop=True)

#name trend according to year
name_boy = top1000[top1000.gender == 'M']
name_girl = top1000[top1000.gender == 'F']

total_name = top1000.pivot_table('prop', index = 'year', columns='name', aggfunc = 'sum')

sub_set = total_name[['Mary', 'John', 'Harry', 'Duke', 'Jane']]
sub_set.plot(subplots=True, title = 'name proportions according to year')

table = top1000.pivot_table('prop', index='year', columns='gender', aggfunc='sum')
table.plot(title='top1000 name proportion')

total_birth.plot(title = 'total birth')

def group_cumsum(group, q=0.5):
    group.sort_values(by='prop', ascending=False)
    return group.prop.cumsum().values.searchsorted(q)

diversity = top1000.groupby(['year', 'gender']).apply(group_cumsum).unstack('gender')
diversity.plot()


