import os
import re
import datetime
from StreamToLogger import StreamToLogger
import logging
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys


def configure_logger():
    logging.basicConfig(filename='./data_loader.log',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.DEBUG)
    stdout_logger = logging.getLogger('STDOUT')
    sl = StreamToLogger(stdout_logger, logging.INFO)
    sys.stdout = sl
    stderr_logger = logging.getLogger('STDERR')
    sl = StreamToLogger(stderr_logger, logging.ERROR)
    sys.stderr = sl


def calculate_correlation(df1, df2):
    correlation_df = pd.merge(df1, df2, on="start")
    correlation_df = correlation_df[["trans", "stem"]]
    cor = correlation_df.corr(method='pearson')
    logging.debug("The correlation table: %s", cor)
    return cor


def save_correlation_plot(summary_df, save_dir):
    #summary_df.sort_values(['stem_name', 'chr'])
    for stem in stems:
        stem_summary_df = summary_df[summary_df['stem_name'] == stem]
        stem_summary_df.sort_values(['chr'])
        ax = sns.barplot(x="chromosome", y="correlation", data=stem_summary_df["chr", "corr"])
        ax.savefig(os.path.join(save_dir, stem + ".png"))


# A logger configuration
configure_logger()

start_time = datetime.datetime.now()
logging.info('The correlation calculation script started at %s', start_time)

transcription_dir = "./data"
stem_dir = "./stems"
coverage_name_pattern = re.compile("coverage_table_(chr.*)_\.bed")
stems = ["JKD21_KUKU", "Z228X3"]
stem_locations = {"JKD21_KUKU": "./stems/JKD21_KUKU"}   # Stem-loops locations

for path, dirs, files in os.walk(transcription_dir):
    for file in files:
        if coverage_name_pattern.match(file):   # Find coverage files
            summary_df = pd.DataFrame(columns=["chr", "stem_name", "corr"])

            path_to_transcription = os.path.join(path, file)
            transcription_df = pd.read_csv(path_to_transcription, sep='\t',
                                           usecols=[1, -1],              # Read start position and coverage
                                           names=["start", "trans"])
            logging.info("Transcription factor coverage file %s", path_to_transcription)

            for stem_name, stem_location in stem_locations.items():
                path_to_stem = os.path.join(stem_location, file)    # Get stem coverage file by chr name
                stem_df = pd.read_csv(path_to_stem, sep='\t',
                                      usecols=[1, -1],
                                      names=["start", "stem"])
                logging.info("Stem-loop coverage file %s", path_to_stem)
                cor = calculate_correlation(transcription_df, stem_df)
                chr_name = coverage_name_pattern.match(file).group(0)
                summary_df = summary_df.append(pd.DataFrame({'chr': chr_name,
                                                             "stem_name": stem_name,
                                                             "corr": cor[0][1]}))
            save_correlation_plot(summary_df, path)

finish_time = datetime.datetime.now()
logging.info('The correlation calculation script finished at %s', finish_time)
