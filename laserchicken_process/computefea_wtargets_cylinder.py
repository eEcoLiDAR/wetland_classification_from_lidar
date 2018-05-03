"""
@author: Zsofia Koma, UvA and Romulo Goncalves NLeSC
Aim: calculate features using laserchicken within a cylinder

Input: las file
Output: ply file with the calculated features

Steps:
1. Import data
2. Compute neighborhood within the defined cylinder cylinder (kdtree approach) [furthermore target points can be defined == only calculate the feature related selected points but based on the original point cloud, however the results only linked back to the target point -- here the target point == environment point which means we calculated the neighborhood point by point]
3. Feature calculation 
4. Export

Example usage (from command line): python computefea_wtargets_cylinder.py <path>/laserchicken/ <path of data>/_testdata/testdata.las <path of data>/_testdata/testdata.las 2.5 <path of data>/testdata_fea.ply

ToDo: 
"""

import argparse
import time
import numpy as np

import sys

parser = argparse.ArgumentParser()
parser.add_argument('path_of_laserchicken', help='The path of laserchicken')
parser.add_argument('input', help='absolute path of input point cloud (las file)')
parser.add_argument('target', help='absolute path of target points (las file)')
parser.add_argument('radius', help='radius of the volume (a float number)')
parser.add_argument('output', help='absolute path of output point cloud')
args = parser.parse_args()

sys.path.insert(0, args.path_of_laserchicken)

from laserchicken import read_las
from laserchicken.keys import point
from laserchicken.volume_specification import InfiniteCylinder
from laserchicken.compute_neighbors import compute_neighborhoods
from laserchicken.feature_extractor import compute_features
from laserchicken.write_ply import write

print("------ Import is started ------")

pc = read_las.read(args.input)
target = read_las.read(args.target)

print(("Number of points: %s ") % (pc[point]['x']['data'].shape[0]))
print(("Number of points in target: %s ") % (target[point]['x']['data'].shape[0]))

print("------ Computing neighborhood is started ------")

start = time.time()

#compute_neighborhoods is now a generator. To get the result of a generator the user
#needs to call next(compute_neighborhoods). The following shows how to get the results.
#
#indices_cyl=compute_neighborhoods(pc, target, InfiniteCylinder(np.float(args.radius)))
#

neighbors=compute_neighborhoods(pc, target, InfiniteCylinder(np.float(args.radius)))
iteration=0
target_idx_base=0
for x in neighbors:
  end = time.time()
  difftime=end - start
  print(("build kd-tree: %f sec") % (difftime))
  print("Computed neighborhoods list length at iteration %d is: %d" % (iteration,len(x)))

  start1 = time.time()
  print("------ Feature calculation is started ------")
  compute_features(pc, x, target_idx_base, target, ['max_z','echo_ratio','eigenv_1', 'eigenv_2', 'eigenv_3',
  'normal_vector_1','normal_vector_2','normal_vector_3','slope','pulse_penetration_ratio','sigma_z'], InfiniteCylinder(np.float(args.radius)))
  target_idx_base+=len(x)
  end1 = time.time()
  difftime1=end1 - start1
  print(("feature calc: %f sec") % (difftime1))
  iteration+=1


write(target,args.output)
