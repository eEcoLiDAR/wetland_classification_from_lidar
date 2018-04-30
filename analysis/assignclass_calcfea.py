"""
@author: Zsofia Koma, UvA
Aim: assign the validation data to the segmentation results

Input: validation data (digitized shapefile) and segmentation results saved as point shape file
Output: point shape file with class label

Example usage (from command line):   python assignclassvalues.py D:/Geobia_2018/Lauw_island_tiles/ vlakken_union_structuur test2points

ToDo: 
1. highest score in the case of big segment not always representative 

"""

import sys
import argparse

import numpy as np
import pandas as pd
import geopandas as gpd

from shapely.geometry import Point, Polygon
from geopandas.tools import sjoin


parser = argparse.ArgumentParser()
parser.add_argument('path', help='where the files are located')
parser.add_argument('validation', help='name of polygon')
parser.add_argument('segments_point', help='name of the shp file with segmentID (points)')
parser.add_argument('segments_poly', help='name of the shp file with segmentID (poly)')
parser.add_argument('features', help='point cloud with features')
args = parser.parse_args()

# read the validation polygon and segmentation results (point shape file)

print("------ Import data------ ")

crs = {'init': 'epsg:28992'}

validation = gpd.GeoDataFrame.from_file(args.path+args.validation+'.shp',crs=crs)
segments_point = gpd.GeoDataFrame.from_file(args.path+args.segments_point+'.shp',crs=crs)
segments_poly = gpd.GeoDataFrame.from_file(args.path+args.segments_poly+'.shp',crs=crs)

pc_wfea =pd.read_csv(args.path+args.features,sep=',',names=['X','Y','Z','echo_ratio','Planarity','Sphericity','Curvature','kurto_z','max_z','mean_z','median_z','pulse_penetration_ratio','range','sigma_z','skew_z','std_z','var_z'])
pc_wfea['geometry'] = pc_wfea.apply(lambda z: Point(z.X, z.Y), axis=1)
pc_wfea = gpd.GeoDataFrame(pc_wfea,crs=crs)

# spatial join between segmentation results and validation data

print("------ Spatial join ------ ")
pointInPolys = sjoin(segments_point , validation, how='left',op='within')
#pointInPolys.drop_duplicates('value')

# vote for the most frequently presented class

print("------ Voting and labeling the data------ ")

pointInPolys['Open water'] = pointInPolys.groupby('value')['structyp_e'].transform(lambda x: x[x.str.contains('Open water')].count())
pointInPolys['Struweel'] = pointInPolys.groupby('value')['structyp_e'].transform(lambda x: x[x.str.contains('Struweel')].count())
pointInPolys['Bos'] = pointInPolys.groupby('value')['structyp_e'].transform(lambda x: x[x.str.contains('Bos')].count())
pointInPolys['Grasland'] = pointInPolys.groupby('value')['structyp_e'].transform(lambda x: x[x.str.contains('Grasland')].count())
pointInPolys['Landriet, structuurrijk'] = pointInPolys.groupby('value')['structyp_e'].transform(lambda x: x[x.str.contains('Landriet, structuurrijk')].count())
pointInPolys['Landriet, structuurarm'] = pointInPolys.groupby('value')['structyp_e'].transform(lambda x: x[x.str.contains('Landriet, structuurarm')].count())
pointInPolys['Waterriet'] = pointInPolys.groupby('value')['structyp_e'].transform(lambda x: x[x.str.contains('Waterriet')].count())

pointInPolys['Highestfreq'] = pointInPolys[['Open water','Struweel','Bos','Grasland','Landriet, structuurrijk','Landriet, structuurarm','Waterriet']].max(axis=1)
pointInPolys['Sumfreq'] = pointInPolys[['Open water','Struweel','Bos','Grasland','Landriet, structuurrijk','Landriet, structuurarm','Waterriet']].sum(axis=1)
pointInPolys['Highestid'] = pointInPolys[['Open water','Struweel','Bos','Grasland','Landriet, structuurrijk','Landriet, structuurarm','Waterriet']].idxmax(axis=1)

pointInPolys['Prob'] = pointInPolys['Highestfreq']/ pointInPolys['Sumfreq']

# Assign classes to segment polygon

print("------ Assign classes to segment polygon ------ ")

labeled_segments = segments_poly.merge(pointInPolys[['value','Highestfreq','Sumfreq','Highestid','Prob']], on='value')
labeled_segments=labeled_segments.drop_duplicates('value')

# Assign aggregated features to polygon

print("------ Calculate segment-based features (mean, std) ------ ")

segment_polywfea = sjoin(pc_wfea , segments_poly, how='left',op='within')
segment_polywfea.to_file(args.path+args.segments_poly+".point_wfea_wlabel.shp", driver='ESRI Shapefile')

# Calculate aggregated statistical features
fea_insegments_mean=segment_polywfea.groupby('value')['echo_ratio','Planarity','Sphericity','Curvature','kurto_z','max_z','mean_z','median_z','pulse_penetration_ratio','range','sigma_z','skew_z','std_z','var_z'].mean().add_prefix('mean_').reset_index()
fea_insegments_std=segment_polywfea.groupby('value')['echo_ratio','Planarity','Sphericity','Curvature','kurto_z','max_z','mean_z','median_z','pulse_penetration_ratio','range','sigma_z','skew_z','std_z','var_z'].std(ddof=0).add_prefix('std_').reset_index()

fea_insegments1 = fea_insegments_mean.merge(fea_insegments_std, on='value')
fea_insegments = fea_insegments1.drop_duplicates('value')

# Calculate shape geometry features
labeled_segments['poly_area']=labeled_segments['geometry'].area

# Export

print("------ Export ------ ")

feawith_segments = labeled_segments.merge(fea_insegments, on='value')
feawith_segments.drop_duplicates('value').to_file(args.path+args.segments_poly+".wfea_wlabel.shp", driver='ESRI Shapefile')



