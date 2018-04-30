:: Aim: execute segmentation using GRASS GIS
:: Previously necessary to set up the mapset with XY Descartes not specified coordinate system (the last parameter during the execution is the place where the PERMANENT directory is located)
:: Usage example:  C:/OSGeo4W64/bin/grass74.bat --exec D:/GitHub/eEcoLiDAR/myPhD_escience_analysis/grassgis_process/grass_segmentation.bat D:/Geobia_2018/Results_12ofApril/GrassGIS/LauMeer

set filepath=%2
set filename=%3

set n=%4 
set s=%5 
set e=%6 
set w=%7

set thres=%8
set minsize=%9

:: set region
g.region n=%n% s=%s% e=%e% w=%w%

:: import data
r.in.xyz --overwrite input=%filepath%%filename%.csv output=%filename%_PC1 separator=, skip=1 value_column=4
r.in.xyz --overwrite input=%filepath%%filename%.csv output=%filename%_PC2 separator=, skip=1 value_column=5
r.in.xyz --overwrite input=%filepath%%filename%.csv output=%filename%_PC3 separator=, skip=1 value_column=6

:: segmentation
i.group --overwrite group=%filename%_groupPCs input=%filename%_PC1,%filename%_PC2,%filename%_PC3
i.segment --overwrite group=%filename%_groupPCs output=%filename%_groupPCs_%thres%_%minsize% threshold=%thres% minsize=%minsize% goodness=%filename%_groupPCs_%thres%_%minsize%_goodness

:: export rasters
r.out.gdal --overwrite input=%filename%_groupPCs_%thres%_%minsize% output=%filepath%%filename%_groupPCs_%thres%_%minsize%.tif
r.out.gdal --overwrite input=%filename%_groupPCs_%thres%_%minsize%_goodness output=%filepath%%filename%_groupPCs_%thres%_%minsize%_goodness.tif

:: export vectors
r.to.vect --overwrite -s input=%filename%_groupPCs_%thres%_%minsize% output=groupPCs_poly type=area
v.out.ogr --overwrite input=groupPCs_poly type=area output=%filepath%%filename%_groupPCs_poly_%thres%%minsize%.shp format=ESRI_Shapefile
r.to.vect --overwrite -s input=%filename%_groupPCs_%thres%_%minsize% output=groupPCs_point type=point
v.out.ogr --overwrite input=groupPCs_point type=point output=%filepath%%filename%_groupPCs_point_%thres%%minsize%.shp format=ESRI_Shapefile