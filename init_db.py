"""Initialise tables in the database"""

import sqlite3


if __name__ == "__main__":
    connection = sqlite3.connect("hierarchical.db")
    cursor = connection.cursor()

    cursor.execute(
        """--sql
        CREATE TABLE Employee(
            ID int not null,
            bossID int,
            name varchar(40) not null,
            primary key (ID),
            foreign key (bossID) references Employee(ID)
        );
        """
    )

    cursor.close()
    connection.close()
