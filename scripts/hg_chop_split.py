import subprocess
import resources.configs.prod_config as cnfg

chop_size = cnfg.chop_size
hg_dir = cnfg.hg_dir

subprocess.call(["./sh/hg_chop_split.sh %s %s" % (chop_size, hg_dir)], shell=True)
