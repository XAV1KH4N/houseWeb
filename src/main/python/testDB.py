import sqlite3


def connect():
    address = "/home/xavi/websites/houseWeb/src/main/resources/Database.db"
    conn = sqlite3.connect(address)
    cursor = conn.cursor()

if __name__ == '__main__':
    try:
        connect()
        print("All good")
    except Exception as e:
        print("@@Error connecting")
        print(e)