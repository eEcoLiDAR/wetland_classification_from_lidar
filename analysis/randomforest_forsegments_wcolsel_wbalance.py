"""
@author: Zsofia Koma, UvA
Aim: apply Random Forest for classifying segments into given vegetation classes

Input: path of polygon with segment related features + label
Output: accuracy report, feature importance, classified shapefile 

Example usage (from command line): 

ToDo: 
1. automatize feature_list definition
"""

import sys
import argparse

import numpy as np
import pandas as pd
import geopandas as gpd
from geopandas.tools import sjoin

from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score,precision_score,recall_score
from sklearn.metrics import classification_report

from collections import Counter
from imblearn.under_sampling import RandomUnderSampler

import matplotlib.pyplot as plt
import seaborn as sns

def cohenkappa_calc(cm):
    """
    Cohen Kappa calculator.

    Input: confusion_matrix function from sklearn results
    Output: cohen kappa
    """

    import numpy as np
    sum_diag=sum(cm.diagonal())

    sum_rows=np.ones((1,len(cm)))
    sum_cols=np.ones((len(cm)+1,1))
    bychance=np.ones((1,len(cm)))

    for k in range(0,len(cm)):
        sum_rows[0,k]=sum(cm[:,k])

    for h in range(0,len(cm)):
        sum_cols[h,0]=sum(cm[h,:])

    sum_cols[len(cm),0]=sum(sum_cols)-1

    for j in range(0,len(cm)):
        bychance[0,j]=(sum_rows[0,j]/sum_cols[len(cm),0])*sum_cols[j,0]

    sum_bychance=sum(bychance[0,:])

    cohenkappa=(sum_diag-sum_bychance)/((sum_cols[len(cm),0])-sum_bychance)

    sumsum=np.concatenate((cm, sum_rows), axis=0)
    sumsum2=np.concatenate((sumsum, sum_cols), axis=1)

    return cohenkappa

#################################################################################################

parser = argparse.ArgumentParser()
parser.add_argument('path', help='where the files are located')
parser.add_argument('segments', help='polygon shape file with features and classes')
args = parser.parse_args()

# Import and define feature and label

print("------ Import data and re-organize------ ")

segments = gpd.GeoDataFrame.from_file(args.path+args.segments)
#segments=segments[segments['Highestid']!='Open water']
#segments=segments[segments['Highestid']!='Bos']
segments['Highestid']=segments['Highestid'].replace(['Landriet, structuurarm', 'Landriet, structuurrijk','Waterriet'], 'Riet')

segments['Highestid']=segments['Highestid'].replace(['Riet','Struweel','Grasland'], 'Non-water')


# pre-organize the data

#feature_list=['mean_echo_','mean_Plana','mean_Curva','mean_kurto','mean_sigma','mean_media','mean_Spher']
#feature_list=['mean_echo_','mean_Plana','mean_Curva','mean_kurto','mean_sigma','mean_mean_','mean_media','std_echo_r','std_Planar','std_Curvat','std_kurto_','std_sigma_']
#feature_list=['mean_Plana','mean_Curva','mean_kurto','mean_Spher']
feature_list=segments.columns[7:35]

segments_whighprob=segments[(segments['Prob']>0.7)&(segments['poly_area']>10)]

feature=segments_whighprob[feature_list].values
feature_all=segments[feature_list].values

fea_list_forvis=np.array(feature_list)

label=segments_whighprob['Highestid'].values

# Under-sampling -- get equal number of samples per class + split training and testing

rus = RandomUnderSampler(random_state=0)
feature_resampled, label_resampled = rus.fit_sample(feature, label)
#print(sorted(Counter(label_resampled).items()))

mytrain, mytest, mytrainlabel, mytestlabel = train_test_split(feature_resampled, label_resampled,train_size = 0.6)


# Random Forest

print("------ Apply Random Forest ------ ")

n_estimators=30
criterion='gini'
max_depth=30
min_samples_split=5
min_samples_leaf=5
max_features='auto'
max_leaf_nodes=None
bootstrap=True
oob_score=True
n_jobs=1
random_state=None
verbose=0
class_weight='balanced'

forest = RandomForestClassifier(n_estimators=n_estimators, criterion=criterion, max_depth=max_depth,
                             min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf,
                             max_features=max_features, max_leaf_nodes=max_leaf_nodes, bootstrap=bootstrap, oob_score=oob_score,
                             n_jobs=n_jobs, random_state=random_state, verbose=verbose,class_weight=class_weight)

RF_classifier = forest.fit(mytrain, mytrainlabel)

# Validation

print("------ Validation ------ ")

mypredtest=RF_classifier.predict(mytest)

print(classification_report(mytestlabel, mypredtest)) 
print(confusion_matrix(mytestlabel, mypredtest))

mypred=RF_classifier.predict(feature_all)

segments['pred_class']=mypred

segments.to_file(args.path+args.segments+"_RFclass.shp", driver='ESRI Shapefile')

importances=RF_classifier.feature_importances_
indices = np.argsort(importances)[::-1]

# Plot the feature importances of the forest

print("------ Export ------ ")

plt.figure()
plt.title("Feature importances")
plt.bar(range(mytrain.shape[1]), importances[indices],
       color="r", align="center")
plt.xticks(range(mytrain.shape[1]), fea_list_forvis[indices],rotation=45,horizontalalignment='right')
plt.xlim([-1, mytrain.shape[1]])
plt.tight_layout()
#plt.show()
plt.savefig(args.path+args.segments+"_RFclass_feaimp.png")

# Export classification report

with open(args.path+args.segments+"_RFclass_acc.txt", 'w') as f:
	f.write(np.array2string(confusion_matrix(mytestlabel, mypredtest), separator=', '))
	f.write(classification_report(mytestlabel, mypredtest))
	f.write(np.array2string(cohenkappa_calc(confusion_matrix(mytestlabel, mypredtest))))
	f.write(np.array2string(importances[indices]))
