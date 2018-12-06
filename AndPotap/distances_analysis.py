# ===========================================================================
# Notes
# ===========================================================================
"""
(*) This script outputs the clusters in the running strategies observed
    in the data
"""
# ===========================================================================
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ===========================================================================
# Imports
# ===========================================================================
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import multiprocessing
from scipy.spatial import distance_matrix
from AndPotap.Utils.feature_generation import format_correctly
from AndPotap.Utils.feature_generation import add_diffs
from AndPotap.Utils.stochastic_optimization import sgd_all
from AndPotap.Utils.distance import discrepancy_map
from AndPotap.Utils.distance import discrepancy_gradient_total_map
# ===========================================================================
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ===========================================================================
# Files
# ===========================================================================
os.chdir('/Users/andpotap/Documents/Columbia/EDAV/EDAV/AndPotap')
# file_input = './DBs/marathon_2018.csv'
# file_output = './DBs/marathon_2018_clusters.csv'
file_input = './DBs/marathon_2017.csv'
file_output = './DBs/marathon_2017_clusters.csv'
# file_input = './DBs/marathon_2016.csv'
# file_output = './DBs/marathon_2016_clusters.csv'
# file_input = './DBs/marathon_2015.csv'
# file_output = './DBs/marathon_2015_clusters.csv'
# ===========================================================================
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Load the data
# ===========================================================================
# data = pd.read_csv(file_input, nrows=100)  # Read a chunk
data = pd.read_csv(file_input)  # Read all
data = data[data['type'] == 'R']
data = format_correctly(data, verbose=True)
data = add_diffs(data, verbose=True)
np.random.seed(seed=37373)
data = data[data['sec_8'] < 15000]
mask = 5000
mask = np.random.choice(a=data.shape[0], size=mask)
df = data.reindex(mask).copy()
# ===========================================================================
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Format dates into the correct shape
# ===========================================================================
df_out = df.copy()
df_out = df_out.dropna()
all_cols = [col for col in df.columns if 'diff' in col]
x = df_out[all_cols].values
N = x.shape[0]
t0 = time.time()
d = distance_matrix(x=x, y=x)
print(f'\nDistance matrix: {time.time() - t0:6.1f} sec')
# ===========================================================================
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ===========================================================================
# Optimize
# ===========================================================================
x0 = np.random.uniform(low=-100, high=100, size=(N, 2))
pool = multiprocessing.Pool()
kwargs_f = {'d': d, 'pool': pool}
extra_g = {}
x_min, i = sgd_all(func=discrepancy_map,
                   dev_func=discrepancy_gradient_total_map,
                   kwargs_f=kwargs_f,
                   extra_g=extra_g,
                   x0=x0,
                   eta=1.e-3,
                   batch_pct=1,
                   max_iter=500,
                   variant='SGD',
                   size=N,
                   return_vec=False,
                   verbose=True)
# ===========================================================================
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ===========================================================================
# Plot
# ===========================================================================
plt.figure()
plt.scatter(x_min[:, 0], x_min[:, 1])
plt.show()
# ===========================================================================
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ===========================================================================
# Append the coordinates
# ===========================================================================
df_out.loc[:, 'x'] = x_min[:, 0]
df_out.loc[:, 'y'] = x_min[:, 1]
df_out.to_csv(file_output, index=False)
# ===========================================================================
