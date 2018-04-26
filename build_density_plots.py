import os
import re
import pandas as pd
import matplotlib.pyplot as plt

import resources.configs.test_config as cnfg

pattern = re.compile("coverage_table_(chr.*)_\.bed")
data_dir = cnfg.data_dir
stem_loop_dir = cnfg.stem_loops_dir

images = {}
for path, dirs, files in os.walk(stem_loop_dir):
    for file in files:
        if pattern.match(file):
            file_path = os.path.join(path, file)
            df = pd.read_csv(file_path, sep='\t',
                                           usecols=[1, 3],  # Read start position and coverage
                                           names=["start", "coverage"])
            images[pattern.match(file).group(1) + "__" + path.split(os.sep)[-1]] = df
            #ax = df.plot(x='start', y='coverage')

fig, ax = plt.subplots()

for path, dirs, files in os.walk(data_dir):
    for file in files:
        if pattern.match(file):
            file_path = os.path.join(path, file)
            df = pd.read_csv(file_path, sep='\t',
                                           usecols=[1, 3],  # Read start position and coverage
                                           names=["start", "coverage"])

            for s in ['S6-15_L0-10_M1', 'S15-30_L0-10_M5', 'S16-50_L0-10_M3']:
                stem_df = images[pattern.match(file).group(1) + "__" + s]
                stem_df = stem_df.merge(df, on='start')
                ax = stem_df.plot(x='start', y=['coverage_x', 'coverage_y'])
                path_to_save = os.path.join(path, s + "_" + pattern.match(file).group(1) + "_densities.png")
                fig.savefig(path_to_save)
                plt.clf()

#
#
#import numpy as np
#
#x = np.linspace(0, 2 * np.pi)
#y = np.sin(x ** 2)
#
#fig, ax = plt.subplots()
#ax.plot(x, y)
##plt.show()
#
#x = np.linspace(0, 5 * np.pi)
#y = np.sin(x ** 2)
#ax.plot(x, y)
#plt.show()