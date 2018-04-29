import datetime as dt
import os
import re

import logging

import matplotlib.pyplot as plt
plt.switch_backend('agg')
import pandas as pd
import seaborn as sns

sns.set()


import log.log_configurer as log
import resources.configs.config as conf
cnfg = conf.current_config

file_name = os.path.basename(__file__)
log.configure_logger(file_name, cnfg.log_file)

logging.info('The %s started at %s', file_name, dt.datetime.now())

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
logging.info("Stem-loops are collected")

for path, dirs, files in os.walk(data_dir):
    sample_name = os.path.basename(os.path.normpath(path))
    for file in files:
        if pattern.match(file):
            chromosome_name = pattern.match(file).group(1)
            file_path = os.path.join(path, file)
            logging.info("Read %s", file_path)
            df = pd.read_csv(file_path, sep='\t',
                                           usecols=[1, 3],  # Read start position and coverage
                                           names=["start", "coverage"])
            save_dir = os.path.join(path, "density_plots")
            os.makedirs(save_dir, exist_ok=True)
            for s in ['S6-15_L0-10_M1', 'S15-30_L0-10_M5', 'S16-50_L0-10_M3']:
                stem_df = images[chromosome_name + "__" + s]
                stem_df = stem_df.merge(df, on='start')
                stem_df.columns = ['start', 'stem-loop', 'transcription factor']
                ax = stem_df.plot(x='start', y=['stem-loop', 'transcription factor'])
                ax.set_ylabel('density')
                ax.set_title("Stem-loop:" + s + " Tf:" + sample_name + " " + chromosome_name)
                fig = ax.get_figure()
                fig.set_size_inches(11.7, 8.27)
                path_to_save = os.path.join(save_dir, s + "_" + chromosome_name + "_densities.png")
                fig.savefig(path_to_save)
                logging.info("Image save to %s", path_to_save)
                plt.close()

logging.info('The %s finished at %s', file_name, dt.datetime.now())