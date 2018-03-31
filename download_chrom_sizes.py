import subprocess

import resources.configs.prod_config as cnfg

hg_dir = cnfg.hg_dir
fetch_chrom_path = cnfg.fetch_chrom_path

subprocess.call(["./sh/download_chrom_sizes.sh %s %s" % (hg_dir, fetch_chrom_path)], shell=True)
