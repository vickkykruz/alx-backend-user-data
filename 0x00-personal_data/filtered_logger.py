#!/usr/bin/env python3
""" This is a module that call the function filter_datum that returns
the log message obfuscated:
"""


import re
from typing import List


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """ Thia function returns the log message obfuscated """
    for field in fields:
        message = re.sub(f"{field}=.*?{separator}",
                         f"{field}={redaction + separator}", message)
    return message
