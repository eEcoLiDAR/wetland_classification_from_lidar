# Wetland classification using country-wide ALS data

This repository aims to collect all the scripts which was used for wetland classification based on Airborne Laser Scanning data within the [e-EcoLiDAR project](https://www.esciencecenter.nl/project/eecolidar).

## **The content of the directories**

- **analysis**:

These scripts contains the processing steps related to analyse, convert and classify the data.

- **figures**:

Visualization and camera ready figure plot for publication purpose.

- **grassgis_process**:

[GRASS GIS](https://grass.osgeo.org/) batch scripts for segmentation of LiDAR data. 

- **laserchicken_process**:

Using [laserchicken](https://github.com/eEcoLiDAR/laserchicken) point cloud analysis software for extracting features for ALS data. 

- **workflow**:

Bash file for executing the scripts from this repository and build a consistent workflow for processing the ALS data.

- **testdata**:

Small example dataset for testing purpose.  

## **Installation requirements**

Generally the workflow was tested under Windows 10 operation system. The workflow can be run under Linux operation system, however the GRASS GIS section should be adapted.

1. Install Git: https://gitforwindows.org/
Follow the instructions from here: https://escience-academy.github.io/2017-09-06-git-github/#setup

2. Install Anaconda (most preferably the latest version): https://conda.io/docs/user-guide/install/index.html

3. Install GRASS GIS (version 7.2 or above): https://grasswiki.osgeo.org/wiki/Installation_Guide (OSGeo4W installer can be accessed during QGIS installation: https://qgis.org/en/site/forusers/download.html)

### Install laserchicken software

1. Get the software (GitHub repository: https://github.com/eEcoLiDAR/laserchicken)

a.) Clone the repository (official release)

```
git clone https://github.com/eEcoLiDAR/laserchicken.git
```

b.) Download as zip file without using git

2. Install

Within the command line (using the right python version) go to this directory and run the following:

```
pip install .
```

If shapely failed than install it separately:
```
conda install -c conda-forge shapely
```

### Install addons for GRASS GIS

Two addons is required to install for running this workflow. For the installation after starting up GRASS GIS from command line (grass74 -gtext) you can install addons with the following commands:
```
g.extension extension=r.neighborhoodmatrix
g.extension extension=i.segment.uspo
```

## **Usage**

Before running the entire workflow you should check that in the bash file ( wetland_classification_from_lidar/workflow/Workflow_geobia_confpaper.sh
) the defined absolute paths are correct.

- work_folder: where the test files are located (wetland_classification_from_lidar/testdata directory, the results will be saved in this directory too)
- script_path: where the wetland_classification_from_lidar is located
- path_of_laserchicken: this is where the laserchicken repository is located on your computer
- grass_path: location of your GRASS GIS bin directory
- grass_mapset: before running the workflow user should set up a mapset with Descartes coordinate system (run from GRASS GIS command line separately grass74 -gtext and then follow the instructions of the software and do not specify specific projection)

The valid_polygon which is provided within this repository not the original one (just an example digitalization from my side). It only can be used to test whether the workflow is running. Also the test data is a small tile of the study area [from AHN2 laser campaign](http://www.arcgis.com/home/item.html?id=6c898cd924c441d5aea33b3bc6cc117a) only for demonstration. 

```
bash <filepath>/Workflow_geobia_confpaper.sh
```
 


