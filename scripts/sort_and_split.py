import subprocess
import resources.prod_config as cnfg

log_file = cnfg.log_file
data_dir = cnfg.data_dir
script_dir = cnfg.script_dir

subprocess.call(["./sh/sort_and_split.sh",
                 log_file, data_dir, script_dir], shell=True)
