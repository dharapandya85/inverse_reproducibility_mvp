import logging
import os
import datetime
def setup_logger(name,level=logging.INFO):
    logger=logging.getLogger(name)
    logger.setLevel(level)
    logs_dir="logs"
    os.makedirs(logs_dir,exist_ok=True)
    timestamp=datetime.datetime.now().strftime('%Y--%m-%d_%H-%M-%S')
    log_file_path=os.path.join(logs_dir,f"repro_run_{timestamp}.log")

    file_handler=logging.FileHandler(log_file_path)
    file_formatter=logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')
    file_handler.setFormatter(file_formatter)

    console_handler=logging.StreamHandler()
    console_formatter=logging.Formatter('%(levelname)s:%(message)s')
    console_handler.setFormatter(console_formatter)

    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    return logger