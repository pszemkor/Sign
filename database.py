import sqlite3
import datetime

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
    command = 'INSERT INTO %s%s values %s ' % (table_name, columns, values)
    with connection:
        connection.execute(command)

set_up_database_tables()
insert_values(table_name='Log',
              columns=['Date', 'Text'], values=[datetime.date.today(), "this is test"])