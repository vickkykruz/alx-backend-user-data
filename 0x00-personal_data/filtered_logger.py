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


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str] = None):
        """ This is a initializes self method"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields or []

    def format(self, record: logging.LogRecord) -> str:
        """ This filters values in incoming log records using
        filter_datum """
        return filter_datum(self.fields,
                            RedactingFormatter.REDACTION,
                            super(RedactingFormatter, self).format(record),
                            RedactingFormatter.SEPARATOR)
