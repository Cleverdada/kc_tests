#!/usr/bin/env python
# -*-coding:utf-8-*-
import logging


def get_console_logger():
    # create formatter
    fmt = "[%(asctime)s]    [%(name)s]  [%(levelname)s] [%(process)d]   %(message)s"
    datefmt = "%a %d %b %Y %H:%M:%S"
    formatter = logging.Formatter(fmt, datefmt)

    # create logger
    console_logger = logging.getLogger("export")
    console_logger.setLevel(logging.INFO)

    # create stream handler
    sh = logging.StreamHandler()

    # add handler and formatter to logger
    sh.setFormatter(formatter)
    console_logger.addHandler(sh)
    return console_logger