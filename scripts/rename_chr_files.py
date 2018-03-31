import subprocess
import resources.configs.test_config as cnfg

log = cnfg.log_file
data_sample_dir=cnfg.data_sample_dir

subprocess.call(["./sh/rename_chr_files.sh %s %s" % (log, data_sample_dir)], shell=True)
