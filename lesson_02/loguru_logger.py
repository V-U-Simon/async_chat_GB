from loguru import logger

logger.add(
    f"{__name__}.log",
    format="{time} {level} {message}",
    # format="<green>{time}</green> {level} <level>{message}</level>",
    level="DEBUG",
    serialize=True,
)
