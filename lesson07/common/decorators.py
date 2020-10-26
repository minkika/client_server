import traceback


def log_de(f):
    def corator(self, *args, **kwargs):
        self.logger.debug(f'Функция {f.__name__} ({args}, {kwargs}) вызвана из функции '
                          f'{traceback.format_stack()[0].strip().split()[-1]} и вызвала логер')

        return f(self, *args, **kwargs)

    return corator
