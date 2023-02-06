import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("/Users/alv/Documents/Scripts/Teachworks/Teachworks")

    def get(self, sql):
        cursor = self.conn.cursor()
        results = cursor.execute(sql)
        cursor.close()
        return results.fetchall()

    def commit(self, sql):
        cursor = self.conn.cursor()
        cursor.execute(sql)
        self.conn.commit()
        cursor.close()

    