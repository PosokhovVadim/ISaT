import logging


class Logger:
    def __init__(self, file_name=None):
        self.logger = logging.getLogger(file_name)
        self.logger.setLevel(logging.INFO)

        if file_name:
            file_handler = logging.FileHandler(file_name)
            file_handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                )
            )
            self.logger.addHandler(file_handler)
