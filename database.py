import sqlite3

class SQLighter():
    def __init__(self, path):
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()
        print('Соединение установлено')
        db_version = self.cursor.execute('select sqlite_version();').fetchall()
        print(f'Версия базы данных: {db_version}')
        self.cursor.close()