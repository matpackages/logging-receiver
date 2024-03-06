"""Custom logging handlers."""
import datetime as dt
import gzip
import logging.handlers
import os


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


def timestamp_str() -> str:
    """Get timestamp string."""
    return dt.datetime.now(tz=dt.timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")
