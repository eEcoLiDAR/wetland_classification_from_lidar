import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

font = {'family': 'normal',
        'weight': 'bold',
        'size': 18}

plt.rc('font', **font)

workdir='D:/Geobia_2018/Results_17ofApril/'
filename='3all_tiles_clean.txt_PC1__PC2__PC3segm_parameters'

segm_optimal=pd.read_csv(workdir+filename+'.csv',sep=',')

segm_optimal.rename(columns={'Threshold': 'Similarity threshold'}, inplace = True)
print(segm_optimal.dtypes)

segm_optimal=segm_optimal[segm_optimal['Minimum size']!=50]

segm_optimal=segm_optimal.sort_values(by=['Similarity threshold'])

"""
fig, ax = plt.subplots(figsize=(8,6))
segm_optimal.groupby('Minimum size').plot(x='threshold',y='optimization_criteria',ax=ax,marker='o')
plt.show()
"""

sns.pointplot(x='Similarity threshold',y='Optimization criteria',hue='Minimum size',data=segm_optimal,linestyle="-")
plt.show()