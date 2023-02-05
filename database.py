import sqlite3

class Database:
    def __init__(self):
        self.cur = sqlite3.connect("/Users/alv/Documents/Scripts/Teachworks/Teachworks")

    def get(self, sql):
        results = self.cur.execute(sql)
        return results.fetchall()

    def commit(self, sql):
        self.cur.execute(sql)
    