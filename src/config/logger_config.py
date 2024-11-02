import logging
from logging.handlers import TimedRotatingFileHandler
from fastapi.logger import logger
import os
 
logger.setLevel(logging.DEBUG)
 
logger_dir_relative_path = 'src/logging'
current_directory = os.getcwd()
logger_dir_absolute_path = os.path.join(current_directory, logger_dir_relative_path)
os.makedirs(logger_dir_absolute_path, exist_ok=True)
 
# Create a file handler
fileHandler = TimedRotatingFileHandler('src/logging/app.log', backupCount=10, when='midnight', interval=1)
fileHandler.setLevel(logging.DEBUG)
fileHandler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
fileHandler.namer = lambda name: name.replace("app.log", "") + '_combined.log'
logger.addHandler(fileHandler)
 
# Disable propagation to avoid duplication of logs
logger.propagate = False
new_logger = logger