#!/usr/bin/env python3
"""
Regex-ing
Log formatter
Create logger
Connect to secure database
Read and filter data
"""

import logging
import re
import os
import mysql.connector
from typing import List

PII_FIELDS = ('email', 'phone', 'ssn', 'password', 'ip')


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        """Constructor method"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filter values in incoming log records using filter_datum"""
        message = super(RedactingFormatter, self).format(record)
        redacted_msg = filter_datum(self.fields, self.REDACTION,
                                    message, self.SEPARATOR)
        return redacted_msg


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Returns the log message obfuscated"""
    pattern = r'(' + '|'.join(map(re.escape, fields)) + r')=' +\
        r'[^' + re.escape(separator) + r']+'
    return re.sub(pattern, r'\1=' + redaction, message)


def get_logger() -> logging.Logger:
    """Returns a logging.Logger object."""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    formatter = RedactingFormatter(PII_FIELDS)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Returns a connector to the database"""
    db_username = os.getenv('PERSONAL_DATA_DB_USERNAME') or "root"
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')
    db_password = os.getenv('PERSONAL_DATA_DB_PASSWORD') or ""
    db_host = os.getenv('PERSONAL_DATA_DB_HOST') or "localhost"
    connection = mysql.connector.connect(user=db_username,
                                         password=db_password, host=db_host,
                                         database=db_name)
    return connection


def main():
    """
    Obtain a database connection using get_db and
    retrieve all rows in the users table
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    filtered_fields = ['name', 'email', 'phone', 'ssn', 'password']

    logging.basicConfig(format='[HOLBERTON] user_data INFO: %(message)s',
                        level=logging.INFO)

    # Log each row under filtered format
    for row in rows:
        filtered_row = {key: '***' if key in filtered_fields else value
                        for key, value in zip(cursor.column_names, row)}
        logging.info("; ".join([f"{key}={value}" for key, value in
                                filtered_row.items()]))

    cursor.close()
    db.close()


cursor = None


if __name__ == "__main__":
    main()
