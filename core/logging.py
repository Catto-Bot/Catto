import logging
from logging.handlers import RotatingFileHandler

_logger = logging.getLogger("catto")


def configure() -> None:
    if _logger.handlers:
        return
    _logger.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    file_handler = RotatingFileHandler("logs.txt", maxBytes=1_000_000, backupCount=3)
    file_handler.setFormatter(fmt)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(fmt)
    _logger.addHandler(file_handler)
    _logger.addHandler(stream_handler)


def log_command(ctx) -> None:
    guild = ctx.guild.name if ctx.guild else "DM"
    _logger.info("%s used in '%s' by %s", ctx.command.name, guild, ctx.author)
