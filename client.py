"""Example client that sends some log records to the server.

Usage: python3 client.py <server> <port>
Example: python3 client.py localhost 9000
"""
import logging
import logging.handlers
import logging.config
import sys


def main():
    """Main function."""
    server = sys.argv[1] if len(sys.argv) > 1 else "localhost"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 9000
    logging.config.dictConfig(config=get_config(server, port))
    sample_logs()


def get_config(server, port):
    """Return logging config dict."""
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "socket_handler": {
                "class": "logging.handlers.SocketHandler",
                "host": server,
                "port": port
            },
            "stderr": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "stream": "ext://sys.stderr"
            },
        },
        "loggers": {
            "root": {
                "level": "DEBUG",
                "handlers": ["socket_handler", "stderr"]
            }
        }
    }


def sample_logs():
    """Create some example log records."""

    logger = logging.getLogger('myapp')
    logger.info("Jackdaws love my big sphinx of quartz.")

    logger1 = logging.getLogger('myapp.area1')
    logger2 = logging.getLogger('myapp.area2')

    logger1.debug("Quick zephyrs blow, vexing daft Jim.")
    logger1.info("How quickly daft jumping zebras vex.")
    logger2.warning("Jail zesty vixen who grabbed pay from quack.")
    logger2.critical("A failure occurred.")
    logger2.error("The five boxing wizards jump quickly.", extra={"a_num": 42})

    try:
        1 / 0
    except ZeroDivisionError:
        info = {"even_more": 14.8, "user": "john"}
        logger.exception("exception message", extra=info)


if __name__ == '__main__':
    main()
