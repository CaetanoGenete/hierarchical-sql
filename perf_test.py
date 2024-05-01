"""Compare simple recursive vs iterative"""

import sqlite3
from timeit import timeit
import create_tree


connection = sqlite3.connect("hierarchical.db")
cursor = connection.cursor()


TEST_EMP = 100000 - 1


def recursive_benchmark():
    """Bench using recursive query"""

    cursor.execute(
        """--sql
        WITH RECURSIVE bosses(id, bossID, name) AS (
            SELECT
                id,
                bossID,
                name
            FROM
                Employee WHERE id = ?
            UNION ALL
            SELECT
                emp.id,
                emp.bossID,
                emp.name
            FROM Employee emp
            INNER JOIN bosses on bosses.bossID = emp.id
        )
        SELECT * FROM bosses;
        """,
        [(TEST_EMP)],
    )


def _get_boss(emp_id: int) -> tuple[str, int]:
    result = cursor.execute(
        "SELECT name, bossID FROM Employee WHERE id = ?", [(emp_id)]
    )
    return result.fetchone()


def iterative_benchmark():
    """Bench using sequential queries"""

    boss = _get_boss(TEST_EMP)
    while boss[1] is not None:
        boss = _get_boss(boss[1])


if __name__ == "__main__":
    emp_list = create_tree.build_company_hierarchy(100000, unique=False)
    create_tree.persist_employees(emp_list)

    print("recursive: ", timeit("recursive_benchmark()", number=1, globals=globals()))
    print("iterative: ", timeit("iterative_benchmark()", number=1, globals=globals()))
