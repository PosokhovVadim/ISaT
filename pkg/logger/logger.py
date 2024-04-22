import logging
import os


class Logger:
    def __init__(self, file_name=None):
        self.logger = logging.getLogger(file_name)
        self.logger.setLevel(logging.INFO)

        if not os.path.exists("logs"):
            os.makedirs("logs")

        if file_name:
            file_name = os.path.join("logs", file_name)
            file_handler = logging.FileHandler(file_name)
            file_handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                )
            )
            self.logger.addHandler(file_handler)
