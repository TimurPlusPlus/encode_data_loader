import logging
import sys

from log.StreamToLogger import StreamToLogger


def configure_logger(script_name, log_file):
    stdout_logger = logging.getLogger(script_name)
    sl = StreamToLogger(stdout_logger, logging.INFO)
    sys.stdout = sl

    stderr_logger = logging.getLogger(script_name)
    slE = StreamToLogger(stderr_logger, logging.ERROR)
    sys.stderr = slE

    logging.basicConfig(filename=log_file,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.DEBUG)
