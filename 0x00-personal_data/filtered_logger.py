#!/usr/bin/env python3
""" This is a module that call the function filter_datum that returns
the log message obfuscated:
"""


import re


def filter_datum(fields, redaction, message, separator):
    """ This is rwturn the value of the paaaes parameter """

    return re.sub(
            rf"(?:{separator})({'|'.join(fields)})=(.*?){separator}",
            rf"\1={redaction}\2", message)
