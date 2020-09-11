import pyodbc

# DB connection properties
dbs = [
    {
        "server": 'localhost',
        "db_name": 'db01',
        "username": '',
        "password": '',
        "driver": '{ODBC Driver 13 for SQL Server}',
        "tables": [
            'table_01',
            'table_02',
            'table_03',
            'table_04',
            'table_05'
        ]
    },
    {
        "server": 'localhost',
        "db_name": 'db02',
        "username": '',
        "password": '',
        "driver": '{ODBC Driver 13 for SQL Server}',
        "tables": [
            'table_01',
            'table_02',
            'table_03',
            'table_04',
            'table_05'
        ]
    }
]

def db_table_dump(connection, table_name):
    cursor = connection.cursor()

    sql_command = "SELECT * FROM " + table_name + " e"

    cursor.execute(sql_command)

    row = cursor.fetchone()

    while row:
        text = ''

        for field in row:
            if len(text) != 0:
                text = text + "\t|\t"

            text = text + str(field)

        print(text)

        row = cursor.fetchone()

    cursor.close()

    del cursor

def db_dump(connection, db_info):
    print("[DB: " + db_info['db_name'] + "]")

    for table_name in db_info['tables']:
        print('[TABLE: ' + table_name + ']')

        db_table_dump(connection, table_name)

def main(dbs):
    for db_info in dbs:
        # DB connection
        db_connection_str = 'DRIVER=' + db_info['driver'] + ';SERVER=' + db_info['server'] + ';PORT=1443;DATABASE=' + db_info['db_name'] + ';UID=' + db_info['username'] + ';PWD=' + db_info['password'];

        connection = pyodbc.connect(db_connection_str)

        db_dump(connection, db_info)

        connection.close()

if __name__ == "__main__":
    main(dbs)
