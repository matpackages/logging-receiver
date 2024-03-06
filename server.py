"""Logging receiver server."""
import datetime as dt
import gzip
import json
import logging
import logging.handlers
import logging.config
import os
import pickle
import select
import socketserver
import struct


class LogRecordStreamHandler(socketserver.StreamRequestHandler):
    """Handler for a streaming logging request.

    This basically logs the record using whatever logging policy is
    configured locally.
    """

    def handle(self):
        """
        Handle multiple requests - each expected to be a 4-byte length,
        followed by the LogRecord in pickle format. Logs the record
        according to whatever policy is configured locally.
        """
        while True:
            chunk = self.connection.recv(4)
            if len(chunk) < 4:
                break
            slen = struct.unpack('>L', chunk)[0]
            chunk = self.connection.recv(slen)
            while len(chunk) < slen:
                chunk = chunk + self.connection.recv(slen - len(chunk))
            obj = self._unpickle(chunk)
            record = logging.makeLogRecord(obj)
            self._handle_log_record(record)

    def _unpickle(self, data):
        """Decode log record in pickle format."""
        return pickle.loads(data)

    def _handle_log_record(self, record):
        """Handle log record."""
        # if a name is specified, we use the named logger rather than the one
        # implied by the record.
        if self.server.logname is not None:
            name = self.server.logname
        else:
            name = record.name
        logger = logging.getLogger(name)
        # N.B. EVERY record gets logged. This is because Logger.handle
        # is normally called AFTER logger-level filtering. If you want
        # to do filtering, do it at the client end to save wasting
        # cycles and network bandwidth!
        logger.handle(record)


class LogRecordSocketReceiver(socketserver.ThreadingTCPServer):
    """
    Simple TCP socket-based logging receiver suitable for testing.
    """

    allow_reuse_address = True

    def __init__(self, host='0.0.0.0',
                 port=logging.handlers.DEFAULT_TCP_LOGGING_PORT,
                 handler=LogRecordStreamHandler):
        socketserver.ThreadingTCPServer.__init__(self, (host, port), handler)
        self.abort = 0
        self.timeout = 1
        self.logname = None

    def serve_until_stopped(self):
        """Start server."""
        abort = 0
        while not abort:
            rd, _, _ = select.select(
                [self.socket.fileno()],
                [],
                [],
                self.timeout
            )
            if rd:
                self.handle_request()
            abort = self.abort


def load_config():
    """Load JSON config."""
    with open("config.json", "r", encoding="utf-8") as f:
        return json.load(f)


def timestamp_str() -> str:
    """Get timestamp string."""
    return dt.datetime.now(tz=dt.timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")


class GzipRotator:
    """File rotator with gzip compression and timestamped naming."""

    def __call__(self, source, dest):
        """Compress file using gzip."""
        # https://stackoverflow.com/a/16461440
        ext = ".jsonl"
        dest = source.replace(ext, "") + "." + timestamp_str() + ext
        os.rename(source, dest)
        new_name = f"{dest}.gz"
        with open(dest, 'rb') as f_in, gzip.open(new_name, 'wb') as f_out:
            f_out.writelines(f_in)
            f_out.close()
            f_in.close()
            os.remove(dest)


class CompressedRotatingFileHandler(logging.handlers.RotatingFileHandler):
    """RotatingFileHandler with compression on rotate and timestamp file name.

    Keeps an unlimited number of backups if backupCount > 0.
    """

    rotator = GzipRotator()


def main():
    """Main function."""
    logging.config.dictConfig(config=load_config())

    tcpserver = LogRecordSocketReceiver(port=9000)
    print('Starting TCP server.')
    tcpserver.serve_until_stopped()


if __name__ == '__main__':
    main()
