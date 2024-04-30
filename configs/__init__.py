import logging
from logging.config import dictConfig
from logging.handlers import RotatingFileHandler

class ContextFilter(logging.Filter):
    def filter(self, record):
        record.module_name = __name__
        return True

dictConfig({
    'version': 1,
    'filters': {
        'context_filter': {
            '()': ContextFilter,
        },
    },
    'formatters': {
        'detailed': {
            'format': '%(asctime)s - %(name)s - (%(filename)s:%(lineno)d, %(funcName)s) - [%(levelname)s] - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s - %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'WARNING',
            'formatter': 'simple',
            'stream': 'ext://sys.stdout',
            'filters': ['context_filter'],
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'detailed',
            'filename': 'app.log',
            'maxBytes': 1024*1024*5,
            'backupCount': 10,
            'encoding': 'utf8',
            'filters': ['context_filter'],
        },
    },
    'loggers': {
        'my_module': {
            'level': 'DEBUG',
            'handlers': ['console', 'file'],
            'propagate': False
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console', 'file']
    },
})

def get_logger(name):
    return logging.getLogger(name)