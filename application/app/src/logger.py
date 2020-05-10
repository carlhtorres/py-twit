import logging.config, os


class Logger:
    logging.config.fileConfig(f'{os.getcwd()}/log.conf')
    __logger = logging.getLogger('mainLogger')

    @property
    def logger(self):
        return Logger.__logger
