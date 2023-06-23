import logging


class FolderSynchronizerLogger:
    def log(self, message: str):
        logging.info(message)
        print(message)
