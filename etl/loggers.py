import logging


def setup_logger(log_file: str, level=logging.DEBUG) -> logging.Logger:
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger = logging.getLogger("app_logger")
    logger.setLevel(level)

    if not logger.handlers:
        logger.addHandler(file_handler)
        # logger.addHandler(stream_handler)

    return logger
