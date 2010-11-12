import uno  # everything works well if you uncomment this line
import logging

# Django's trick for older Python versions:
try:
    from logging.config import dictConfig
except ImportError:
    from django.utils.dictconfig import dictConfig

dictConfig({
    'version': 1,
    'handlers': {
        'console':{
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
        },
    },
    'loggers': {
        'my': {
            'handlers': ['console'],
            'level': 'INFO',
        }
    }
})

logger = logging.getLogger('my')
logger.info("Hello world")

