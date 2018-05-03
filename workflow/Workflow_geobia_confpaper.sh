: '
@author: Zsofia Koma, UvA
Aim: pipeline for processing ALS data for wetland classification 

Main workflow steps:
1. Derive features using laserchicken
2. Convert data into the right format
3. PCA analysis
4. Segmentation in GRASS GIS
5. Assign validation data
6. Calculate segment-based feature
7. Apply Random Forest classifier

Example usage (from command line):  bash D:/GitHub/eEcoLiDAR/myPhD_escience_analysis/bash_process/Workflow_analysis_geobia.sh

ToDo: 
1. conversion merge all the tiles together it will not work for larger study area
2. too much output (I/O is time consuming task)
3. spatial join should be optimized

Comment:
1. For visualize ply file in CC the comment section should be deleted
'

# set paths
work_folder="D:/GitHub/eEcoLiDAR/wetland_classification_from_lidar/_testdata/"
script_path="D:/GitHub/eEcoLiDAR/wetland_classification_from_lidar/"

path_of_laserchicken="D:/GitHub/eEcoLiDAR/laserchicken_r1/laserchicken/"

grass_path="C:/OSGeo4W64/bin/"
grass_mapset="D:/Geobia_2018/Results_12ofApril/GrassGIS/LauMeer" #should set up beforehand

# set filenames
filename="testdata"
valid_polygon="vlakken_union_structuur"

# set parameters for laserchicken
radius=1
volume=cylinder

# set the boundary of the study area (maxx,minx,maxy,miny)
n=600000
s=597000
e=220000
w=206000

# parametrization of the segmentation 
threshold=0.1
minsize=1

# Calculate features

echo "--------Feature calculation is started--------"

#python $script_path/laserchicken_process/computefea_wtargets_cylinder.py $path_of_laserchicken $work_folder/$filename.las $work_folder/$filename.las $radius $work_folder/$filename.ply

# Convert ply files into cleaned text file and merge it together

echo "--------Conversion is started--------"

#for f in $work_folder*.ply;do python $script_path/analysis/ply_tograss.py ${f%.ply};done
#cat $work_folder*_clean.txt > $work_folder/all_tiles_clean.txt

# PCA analysis and determine most important PCs

echo "--------PCA analysis is started--------"

#python $script_path/analysis/pca_geobia.py $work_folder/all_tiles_clean.txt 

echo "--------Segmentation started--------"

# GRASS GIS segmentation parameter optimization
#$grass_path/grass74.bat --exec $script_path/grassgis_process/grass_workflow_uspo.bat $work_folder all_tiles_clean.txt_PC1__PC2__PC3 $n $s $e $w

# GRASS GIS segmentation
#$grass_path/grass74.bat --exec $script_path/grassgis_process/grass_segmentation_whinwflow.bat $grass_mapset $work_folder all_tiles_clean.txt_PC1__PC2__PC3 $n $s $e $w $threshold $minsize

echo "--------Assign validation data and calculate segment based features --------"

#Assign validation data and calculate segment based features
#python $script_path/analysis/assignclass_calcfea.py $work_folder $valid_polygon all_tiles_clean.txt_PC1__PC2__PC3_groupPCs_point_$threshold$minsize all_tiles_clean.txt_PC1__PC2__PC3_groupPCs_poly_$threshold$minsize all_tiles_clean.txt

echo "--------Classification --------"

python $script_path/analysis/randomforest_forsegments_wcolsel_wbalance.py $work_folder all_tiles_clean.txt_PC1__PC2__PC3_groupPCs_poly_$threshold$minsize.wfea_wlabel.shp

