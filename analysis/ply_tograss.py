"""
@author: Zsofia Koma, UvA
Aim: transform ply into xyz ascii file for further analysis and process

Input: ply with extracted features from laserchicken (pay attention how many lines should be skipped!)
Output: txt with header and xyz + extra attributes

Example usage (from command line): python ply_tograss.py <path>tile_208000_598000_1_1.las.ply

ToDo: 
1. how to get column names automatically?
"""

import sys
import argparse

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

parser = argparse.ArgumentParser()
parser.add_argument('features', help='point cloud with features (path+filename)')
args = parser.parse_args()

# Read ply into pandas data frame 
pc_wfea = pd.read_csv(args.features+'.ply',sep=' ',names=['X','Y','Z','coeff_var_z','density_absolute_mean','echo_ratio','eigenv_1','eigenv_2','eigenv_3','gps_time','intensity','kurto_z','max_z','mean_z',
'median_z','min_z','normal_vector_1','normal_vector_2','normal_vector_3','pulse_penetration_ratio','range','raw_classification','sigma_z','skew_z','slope','std_z','var_z'],skiprows=39)
#print(pc_wfea.dtypes)
#print(pc_wfea.head())

# Delete columns where all value is 0  
pc_wfea = pc_wfea.loc[:, (pc_wfea != 0).any(axis=0)]

# Add some extra attributes (eigenvalues into features) and drop where the value is nan because eigenvalue was 0.0 which means it was not possible to calculate

pc_wfea['Planarity']=(pc_wfea['eigenv_2']-pc_wfea['eigenv_3'])/pc_wfea['eigenv_1']
pc_wfea['Sphericity']=(pc_wfea['eigenv_2']-pc_wfea['eigenv_3'])/pc_wfea['eigenv_1']
pc_wfea['Curvature']=pc_wfea['eigenv_3']/(pc_wfea['eigenv_1']+pc_wfea['eigenv_2']+pc_wfea['eigenv_3'])

pc_wfea = pc_wfea[np.isfinite(pc_wfea['Planarity'])]
pc_wfea = pc_wfea[np.isfinite(pc_wfea['Sphericity'])]
pc_wfea = pc_wfea[np.isfinite(pc_wfea['Curvature'])]

# Clean up
pc_wfea_clean=pc_wfea[['X','Y','Z','echo_ratio','Planarity','Sphericity','Curvature','kurto_z','max_z','mean_z','median_z','pulse_penetration_ratio','range','sigma_z','skew_z','std_z','var_z']]

# Export pandas data frame 
pc_wfea_clean.to_csv(args.features+'_clean.txt',sep=',',index=False,header=False)

