import logging
import logging.handlers
import logging.config

logger = logging.getLogger('myapp')

logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {},
    "formatters": {
        "json": {
            "()": "json_formatter.JsonFormatter",
            "fmt_keys": {
                "level": "levelname",
                "message": "message",
                "timestamp": "timestamp",
                "logger": "name",
                "module": "module",
                "function": "funcName",
                "line": "lineno",
                "thread_name": "threadName"
            }
        }
    },
    "handlers": {
        "socket_handler": {
            "class": "logging.handlers.SocketHandler",
            "host": "localhost",
            "port": 9456
        },
        "stderr": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "json",
            "stream": "ext://sys.stderr"
        },
    },
    "loggers": {
        "root": {"level": "DEBUG", "handlers": ["socket_handler", "stderr"]}
    }
}

logging.config.dictConfig(config=logging_config)

logger.info("Jackdaws love my big sphinx of quartz.")

logger1 = logging.getLogger('myapp.area1')
logger2 = logging.getLogger('myapp.area2')

logger1.debug('Quick zephyrs blow, vexing daft Jim.')
logger1.info('How quickly daft jumping zebras vex.')
logger2.warning('Jail zesty vixen who grabbed pay from quack.')
logger2.error('The five boxing wizards jump quickly.', extra={"a_num": 42})

def function_err():
    try:
        1 / 0
    except ZeroDivisionError:
        logger.exception("exception message", extra={'even_more': 14.8, 'user': 'pat'})

    return 3


function_err()
