import subprocess
import resources.prod_config as cnfg

log_file = cnfg.log_file
hg_dir = cnfg.hg_dir
stem_loops_dir = cnfg.stem_loops_dir

subprocess.call(["./sh/build_coverages.sh",
                 log_file, hg_dir, stem_loops_dir], shell=True)
