import sqlite3
import sys


if __name__ == "__main__":

    connection = sqlite3.connect("hierarchical.db")
    cursor = connection.cursor()

    match sys.argv[1]:
        case "bosslist":
            hierarchy = cursor.execute(
                """--sql
                WITH RECURSIVE bosses(id, bossID, name) AS (
                    SELECT
                        id,
                        bossID,
                        name
                    FROM
                        Employee WHERE name = ?
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
                [(sys.argv[2])],
            )

            print("\x1b[31m")
            print("->".join(emp[2] for emp in hierarchy.fetchall()))
            print("\x1b[0m")

        case "subordinates":
            hierarchy = cursor.execute(
                """--sql
                WITH RECURSIVE subordinates(id, bossID, name) AS (
                    SELECT
                        id,
                        bossID,
                        name
                    FROM
                        Employee WHERE name = ?
                    UNION ALL
                    SELECT
                        emp.id,
                        emp.bossID,
                        emp.name
                    FROM Employee emp
                    INNER JOIN subordinates on subordinates.id = emp.bossID
                )
                SELECT name FROM subordinates;
                """,
                [(sys.argv[2])],
            )

            print("\x1b[31m")
            print(", ".join(emp[0] for emp in hierarchy.fetchall()))
            print("\x1b[0m")

    cursor.close()
    connection.close()
