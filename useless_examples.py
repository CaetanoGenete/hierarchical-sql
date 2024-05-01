"""Fibonacci example recursive query"""

import sqlite3
import sys


if __name__ == "__main__":
    connection = sqlite3.connect("hierarchical.db")
    cursor = connection.cursor()

    result = cursor.execute(
        """--sql
        WITH RECURSIVE fib(f1, f2) AS (
            SELECT 0, 1
            UNION ALL
            SELECT f2, (f1+f2) FROM fib
        )
        SELECT f1 FROM fib LIMIT ?;
        """,
        [(sys.argv[1])]
    )

    print("\x1b[31m")
    print(", ".join(str(emp[0]) for emp in result.fetchall()))
    print("\x1b[0m")

    cursor.close()
    connection.close()
