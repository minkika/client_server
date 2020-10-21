
import log.client_log_config
import log.server_log_config


def log_de(f):
    def corator(self, *args, **kwargs):
        self.logger.debug(f'Функция {f.__name__} ({args}, {kwargs}) вызвала логер')

        return f(self, *args, **kwargs)
    return corator