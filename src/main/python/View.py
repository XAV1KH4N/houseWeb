import sqlite3


class View:
    def __init__(self):
        address = "../resources/Database.db"
        self.conn = sqlite3.connect(address)
        self.cursor = self.conn.cursor()
        self.createTables()

    def createTables(self):
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS viewings(
            view_id INT PRIMARY KEY,
            view_date DATE NOT NULL,
            view_time TIME NOT NULL
        )''')

    def reset(self):
        self.cursor.execute("DROP table IF EXISTS viewings")
        self.conn.commit()
        self.createTables()

    def createViewId(self):
        self.cursor.execute("SELECT max(view_id) FROM viewings")
        data = self.cursor.fetchall()
        if self.isDataEmpty(data):
            return 1
        else:
            return data[0][0] + 1

    def viewCount(self):
        self.cursor.execute("SELECT count(view_id) FROM viewings")
        data = self.cursor.fetchall()

        if self.isDataEmpty(data):
            raise ViewingError("Error while retrieving data")
        return data[0][0]

    def isDataEmpty(self, data):
        return len(data) == 0 or len(data[0]) == 0 or data[0][0] is None

    def close(self):
        self.conn.close()

    def addViewing(self, date, time):
        id = self.createViewId()
        if not self.exists(date, time):
            self.cursor.execute(f"INSERT INTO viewings VALUES({id}, '{date}', '{time}')")
            self.conn.commit()

    def exists(self, date, time):
        self.cursor.execute(f"SELECT 1 FROM viewings WHERE view_date = '{date}' AND view_time = '{time}'")
        data = self.cursor.fetchall()
        return not self.isDataEmpty(data)

    def getViewings(self):
        self.cursor.execute("SELECT * FROM viewings WHERE view_date  >= date('now') ORDER BY view_date")
        data = self.cursor.fetchall()
        return data

    def deleteViewing(self, id):
        self.cursor.execute(f"DELETE FROM viewings WHERE view_id = {id}")
        self.conn.commit()


class ViewingError(Exception):
    # Class to wrap the different exceptions into one class
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
