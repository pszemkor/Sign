import sqlite3
from datetime import date


def with_connection(func):
    def with_connection_(*args, **kwargs):
        database_path = 'sign.db'
        connection = None
        res = None
        try:
            connection = sqlite3.connect(database_path)
            res = func(connection, *args, **kwargs)
        except sqlite3.DatabaseError as e:
            print(e)
        finally:
            if connection:
                connection.close()
        return res

    return with_connection_


@with_connection
def set_up_database_tables(connection):
    with connection:
        connection.execute("PRAGMA foreign_keys = 1")

        set_up_log_table(connection)
        set_up_progress_table(connection)


def set_up_log_table(connection):
    connection.execute('''CREATE TABLE IF NOT EXISTS Log
    (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Date DATE,
        Text TEXT
        );''')


def set_up_progress_table(connection):
    connection.execute('''CREATE TABLE IF NOT EXISTS Progress
    (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Date DATE,
        Sign TEXT,
        Accuracy REAL
        );''')


@with_connection
def insert_values(connection, table_name, columns, values):
    values = tuple(values)
    columns = tuple(columns)
    command = 'INSERT INTO %s %s values %s ' % (table_name, columns, values)
    print(command)
    with connection:
        connection.execute(command)


@with_connection
def insert_log(connection, values):
    values = tuple(values)
    command = 'INSERT INTO Log ("Date", Text) values (?, ?)'
    with connection:
        connection.execute(command, values)


@with_connection
def insert_progress(connection, values):
    values = tuple(values)
    command = 'INSERT INTO Progress ("Date", Sign, Accuracy) values (?, ?, ?)'
    with connection:
        connection.execute(command, values)


set_up_database_tables()
# d = date.today()
# insert_log([d, "this is test"])
# insert_progress([d, "T", 0.4])