"""
"""
from threading import Event, Lock
import logging
from time import gmtime
from logging.handlers import RotatingFileHandler
from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool

webserver = Flask(__name__)


# webserver.task_runner.start()

webserver.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")
webserver.tasks_runner = ThreadPool(webserver.data_ingestor)

webserver.job_counter = 1
webserver.up = True
webserver.finals = 0
webserver.lock = Lock()
webserver.logger = logging.getLogger("logger")
webserver.logger.setLevel(logging.INFO)

handler = RotatingFileHandler("file.log", maxBytes=1024, backupCount=10)
handler.setLevel(logging.INFO)

format = logging.Formatter('%(asctime)s - %(message)s')
format.converter = gmtime


handler.setFormatter(format)
webserver.logger.addHandler(handler)
webserver.logger.info("da, a inceput")
from app import routes
