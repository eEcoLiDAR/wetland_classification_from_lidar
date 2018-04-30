import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

font = {'family': 'normal',
        'weight': 'bold',
        'size': 18}

plt.rc('font', **font)

importance=np.array([0.06870836,0.05689468,0.05652563,0.05641782,0.0539987,0.04901801,
0.04770275,0.04670926,0.04147883,0.0391324,0.03813576,0.03793391,
0.03499066,0.03412103,0.03381606,0.03069236,0.02889141,0.02884648,
0.02832834,0.02797169,0.02620443,0.02612776,0.02514122,0.02428034,0.02360107,0.02273073,0.01160029])

features=np.array(['std(mean z)','mean(pulse pen.)','mean(mean z)','mean(echo rat.)','std(echo rat.)','std(max z)','std(range z)','mean(planarity)','std(pulse pen.)','mean(skew. z)',
'std(std z)','mean(std z)','mean(range z)','mean(max z)','std(sphericity)','mean(sigma z)','std(sigma z)','std(curvature)','polygon area','mean(var. z)','mean(kurtosis z)','mean(curvature)','std(skew. z)','std(med. z)',
'mean(sphericity)','std(kurtosis z)','std(planarity)','mean(med. z)']) 
 
plt.figure()
plt.title("Feature importances")
plt.bar(range(27), importance,
       color="r", align="center")
plt.xticks(range(27),features,rotation=45,horizontalalignment='right')
plt.xlim([-1, 27])
plt.tight_layout()
plt.show()