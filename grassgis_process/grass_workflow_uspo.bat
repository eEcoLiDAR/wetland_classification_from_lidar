:: Aim: execute segmentation optimization (USPO) using GRASS GIS
:: Previously necessary to set up the mapset with XY Descartes not specified coordinate system (the last parameter during the execution is the place where the PERMANENT directory is located)
:: The analyzed thresholds and min sizes should set within the program
:: i.segment.uspo and r.neighborhoodmatrix addons is required (installation process run in grass gis: g.extension extension=<name of package>)

set filepath=%1
set filename=%2

set n=%3 
set s=%4 
set e=%5 
set w=%6

set thres_start=0.1
set thres_stop=0.3
set thres_step=0.1

set minsizes=1,5,10,25

:: set region
g.region n=%n% s=%s% e=%e% w=%w%

:: import data
r.in.xyz --overwrite input=%filepath%%filename%.csv output=%filename%_PC1 separator=, skip=1 value_column=4
r.in.xyz --overwrite input=%filepath%%filename%.csv output=%filename%_PC2 separator=, skip=1 value_column=5
r.in.xyz --overwrite input=%filepath%%filename%.csv output=%filename%_PC3 separator=, skip=1 value_column=6

:: segmentation
i.group group=%filename%_groupPCs input=%filename%_PC1,%filename%_PC2,%filename%_PC3

:: determine test region
g.region -au n=%n% s=%s% e=%e% w=%w% res=1 save=region

i.segment.uspo --overwrite group=%filename%_groupPCs regions=region output=%filepath%%filename%segm_parameters.csv segment_map=segm_uspo threshold_start=%thres_start% threshold_stop=%thres_stop% threshold_step=%thres_step% minsizes=%minsizes% number_best=3 processes=4 memory=4000
