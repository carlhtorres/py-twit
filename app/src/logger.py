import logging
import logging.config


class Logger:
    logging.config.fileConfig('log.conf')
    __logger = logging.getLogger('mainLogger')

    @property
    def logger(self):
        return Logger.__logger
