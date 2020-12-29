from datetime import datetime
import logging.config


def setup():
    log_file_name = datetime.now().strftime('%y-%m-%d,%H:%M:%S')
    logging.config.fileConfig(f'log/{log_file_name}.log')
