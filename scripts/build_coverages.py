import subprocess
import resources.configs.prod_config as cnfg

log_file = cnfg.log_file
hg_dir = cnfg.hg_dir
data_sample_dir = cnfg.data_sample_dir

subprocess.call(["./sh/build_coverages.sh %s %s %s" %
                 (log_file, hg_dir, data_sample_dir)], shell=True)
