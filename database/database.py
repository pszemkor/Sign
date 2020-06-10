import sqlite3



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
def set_up_database(connection):
    with connection:
        set_up_progress_table(connection)


def set_up_progress_table(connection):
    connection.execute('''CREATE TABLE IF NOT EXISTS Progress
    (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Date DATETIME,
        Sign TEXT,
        TryCount INTEGER,
        Success INTEGER 
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
def insert_progress(connection, values):
    values = tuple(values)
    command = 'INSERT INTO Progress ("Date", Sign, TryCount, Success) values (?, ?, ?, ?)'
    with connection:
        connection.execute(command, values)


@with_connection
def get_progress_table(connection):
    c = connection.cursor()
    c.execute("SELECT * FROM Progress ORDER BY Date DESC LIMIT 100")
    return c.fetchall()


@with_connection
def get_stats_progress_table(connection):
    c = connection.cursor()
    query = '''select Sign,
      (select count(*)
       from Progress as p1
       where p.Sign =p1.Sign and p1.Success=1) as Successes,
      (select count(*)
       from Progress as p2
       where p.Sign =p2.Sign and p2.Success=0) as Failures
    from Progress as p
    group by Sign;'''
    c.execute(query)
    return c.fetchall()


def get_data():
    data = get_progress_table()
    result = []
    for item in data:
        (id, date, sign, count, success) = item
        d = {
            'id': id,
            'date': date,
            'sign': sign,
            'count': count,
            'success': success
        }
        result.append(d)

    return result


def get_stats_data():
    data = get_stats_progress_table()
    result = []
    for item in data:
        (sign, successes, failures) = item
        d = {
            'sign': sign,
            'successes': successes,
            'failures': failures
        }
        result.append(d)
    return result


@with_connection
def delete_stats_data(connection):
    connection.execute("""DELETE FROM Progress;""")
    connection.commit()
