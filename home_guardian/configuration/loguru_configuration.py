import logging
import sys

from loguru import logger

message_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<blue>{thread.name: <15}</blue> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)
print(f"message_format: {message_format}")
# Remove a previously added handler and stop sending logs to its sink.
logger.remove(handler_id=None)
# Set up logging
log_file = "logs/home_guardian.{time}.log"
logger.add(
    log_file,
    level="DEBUG",
    format=message_format,
    enqueue=True,
    # turn to false if in production to prevent data leaking
    backtrace=False,
    rotation="00:00",
    retention="7 Days",
    compression="gz",
    serialize=False,
)
# Override the default stderr
logger.add(sys.stderr, format=message_format)


# Intercept standard logging https://gist.github.com/devsetgo/28c2edaca2d09e267dec46bb2e54b9e2
class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


logging.basicConfig(handlers=[InterceptHandler()], level=0)


def configure() -> None:
    """
    Configure logging.
    """
    logger.warning("Loguru logging configured")