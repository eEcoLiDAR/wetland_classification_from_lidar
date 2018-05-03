"""
@author: Zsofia Koma, UvA
Aim: carry out PCA analysis (and optionally correlation analysis within the features)

Input: cleaned txt (output of ply_tograss.py)
Output: txt with header (X,Y,Z + 3 most important PCs) + plot about correlation matrix and cumulative explained variance vs. PCs

Example usage (from command line): python ply_tograss.py C:/zsofia/Amsterdam/Geobia/Features/ tile_208000_598000_1_1.las.ply

ToDo: 
"""

import sys
import argparse

import math
import numpy as np
import pandas as pd
import geopandas as gpd

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

parser = argparse.ArgumentParser()
parser.add_argument('pcwfea', help='where the files are located')
args = parser.parse_args()

# Import data and clean up

pc_wfea = pd.read_csv(args.pcwfea,sep=',',names=['X','Y','Z','echo_ratio','Planarity','Sphericity','Curvature','kurto_z','max_z','mean_z','median_z','pulse_penetration_ratio','range','sigma_z','skew_z','std_z','var_z'])
#print(pc_wfea.dtypes)

features=pc_wfea[['pulse_penetration_ratio','echo_ratio','Planarity','Sphericity','Curvature','kurto_z','skew_z','std_z','var_z','sigma_z','max_z','mean_z','median_z','range']]

# Extract correlation coefficients

plt.figure(figsize=(10,8))
fig=sns.heatmap(pc_wfea[['pulse_penetration_ratio','echo_ratio','Planarity','Sphericity','Curvature','kurto_z','skew_z','std_z','var_z','sigma_z','max_z','mean_z','median_z','range']].corr(method='pearson'), annot=True, fmt=".2f",xticklabels=1,yticklabels=1)
plt.setp(fig.xaxis.get_majorticklabels(), rotation=25, horizontalalignment='right')
plt.setp(fig.yaxis.get_majorticklabels(), rotation=25, horizontalalignment='right')
plt.tight_layout()
#plt.show()
plt.savefig(args.pcwfea+"_corr_anal.png")
plt.close()


# PCA analysis

z_scaler = StandardScaler()

fea_scaled = z_scaler.fit_transform(features)
pca_anal = PCA().fit(fea_scaled)
features_transf=pca_anal.transform(features) 

variance = pca_anal.explained_variance_ratio_.cumsum()

plt.plot([1,2,3,4,5,6,7,8,9,10,11,12,13,14],variance)
plt.scatter([1,2,3,4,5,6,7,8,9,10,11,12,13,14],variance)
plt.axvline(x=3, color='r', linestyle='-')
plt.ylabel('Cumulative explained variance',fontsize=18)
plt.xlabel('Number of components',fontsize=18)
plt.title('PCA Analysis of the geometrical feature-set',fontsize=18)
plt.style.context('seaborn-whitegrid')
plt.tight_layout()
#plt.show()
plt.savefig(args.pcwfea+"_PCA_anal.png")
plt.close()

#print(features_transf.shape)

# Export the most important PCs

pc_wfea['PC1']=features_transf[:,0]
pc_wfea['PC2']=features_transf[:,1]
pc_wfea['PC3']=features_transf[:,2]

pc_wfea[['X','Y','Z','PC1','PC2','PC3']].to_csv(args.pcwfea+'_PC1_'+'_PC2_'+'_PC3'+'.csv',sep=',',index=False)