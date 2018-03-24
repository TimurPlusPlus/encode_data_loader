import os
import re
import datetime
#from StreamToLogger import StreamToLogger
#import logging
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#import sys


def configure_logger():
    pass
    #logging.basicConfig(filename='./data_loader.log',
    #                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    #                    level=logging.DEBUG)
    #stdout_logger = logging.getLogger('STDOUT')
    #sl = StreamToLogger(stdout_logger, logging.INFO)
    #sys.stdout = sl
    #stderr_logger = logging.getLogger('STDERR')
    #sl = StreamToLogger(stderr_logger, logging.ERROR)
    #sys.stderr = sl


def calculate_correlation(df1, df2):
    correlation_df = pd.merge(df1, df2, on="start")
    correlation_df = correlation_df[["trans", "stem"]]
    cor = correlation_df.corr(method='pearson')
    #logging.debug("The correlation table: %s", cor)
    return cor


stems = ["S15-30_L0-10_M5", "S16-50_L0-10_M3", "S6-15_L0-10_M1"]


def save_correlation_plot(summary_df, save_dir):
    sns.set()
    for stem in stems:
        fig, ax = plt.subplots()
        ax.set_xticklabels(ax.get_xticklabels(), rotation=30)

        fig.set_size_inches(11.7, 8.27)

        stem_summary_df = summary_df[summary_df['stem_name'] == stem]
        stem_summary_df = sort_df(stem_summary_df)

        pal = sns.color_palette("coolwarm", len(stem_summary_df['chr']))
        rank = stem_summary_df['corr'].argsort().argsort()
        sorted_palette = [pal[i] for i in rank]

        sns.barplot(x="chr", y="corr", data=stem_summary_df[["chr", "corr"]],
                    palette=sorted_palette)
        path_to_save = os.path.join(save_dir, stem + ".png")
        fig.savefig(path_to_save)
        #logging.info("A figure saved to %s", path_to_save)


order = ['chr'+str(i) for i in range(1, 23)]
order.extend(['chrX', 'chrY'])


def sort_df(df):
    df['chr'] = pd.Categorical(df['chr'], order)
    return df.sort_values(['chr'])


# A logger configuration
configure_logger()

start_time = datetime.datetime.now()
print(start_time)
#logging.info('The correlation calculation script started at %s', start_time)

transcription_dir = "./data"
stem_dir = "./stems"
coverage_name_pattern = re.compile("coverage_table_(chr.*)_\.bed")
stem_locations = {"S15-30_L0-10_M5": "./stems/S15-30_L0-10_M5",
                  "S16-50_L0-10_M3": "./stems/S16-50_L0-10_M3",
                  "S6-15_L0-10_M1": "./stems/S6-15_L0-10_M1"}   # Stem-loops locations

# Walk through all subdirs in dir
for path, dirs, files in os.walk(transcription_dir):
    # Data frame to aggregate correlations for some assay with all stem-loops
    summary_df = pd.DataFrame(columns=["chr", "stem_name", "corr"])
    for file in files:
        # Find coverage files
        if coverage_name_pattern.match(file):
            path_to_transcription = os.path.join(path, file)
            transcription_df = pd.read_csv(path_to_transcription, sep='\t',
                                           usecols=[1, 2],              # Read start position and coverage
                                           names=["start", "trans"])
            #logging.info("Transcription factor coverage file %s", path_to_transcription)

            for stem_name, stem_location in stem_locations.items():
                path_to_stem = os.path.join(stem_location, file)    # Get stem coverage file by chr name
                stem_df = pd.read_csv(path_to_stem, sep='\t',
                                      usecols=[1, 3],
                                      names=["start", "stem"])
                #logging.info("Stem-loop coverage file %s", path_to_stem)

                cor = calculate_correlation(transcription_df, stem_df)
                chr_name = coverage_name_pattern.match(file).group(1)   # Chromosome name
                summary_df = summary_df.append(pd.DataFrame({'chr': [chr_name],
                                                             "stem_name": [stem_name],
                                                             "corr": [cor['trans']['stem']]}))
    if not summary_df.empty:
        save_correlation_plot(summary_df, path)

finish_time = datetime.datetime.now()
print(finish_time)
#logging.info('The correlation calculation script finished at %s', finish_time)
