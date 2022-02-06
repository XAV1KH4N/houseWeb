import bcrypt
import sqlite3

class Login:
    def __init__(self):
        address = "../resources/dummyDatabase.db"  # This is the database I am testing against, it is temporary
        self.conn = sqlite3.connect(address)
        self.cursor = self.conn.cursor()
        self.createTables()

    def createTables(self):
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS roles(
            view_id INT PRIMARY KEY,
            view_time DATETIME  
        )''')

        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS staff(
            staff_id int PRIMARY KEY,
            first_name VARCHAR(16) NOT NULL, 
            last_name VARCHAR(16) NOT NULL,
            username VARCHAR(16) UNIQUE NOT NULL,
            password VARCHAR(32) NOT NULL,
            role_id int,
            FOREIGN KEY (role_id) REFERENCES Roles(role_id)
            )''')
        self.conn.commit()

    def fillRoles(self):
        # This method was required for testing against a database, it will be removed once there is a database
        # set in place
        try:
            self.cursor.execute("INSERT INTO roles values(?,?,?)", (1, "Waiter", "N/A"))
            self.cursor.execute("INSERT INTO roles values(?,?,?)", (2, "Chef", "N/A"))
            self.cursor.execute("INSERT INTO roles values(?,?,?)", (3, "Manager", "N/A"))
            self.conn.commit()
        except:
            pass

    def createHash(self, password):
        # This method creates a hash using a randomly generated salt, two identical passwords will
        # have different hashes
        encoded = str.encode(password)
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(encoded, salt)
        # The hash is returned in bytes not a string
        return hashed

    def confirmHash(self, password, hash):
        try:
            password = str.encode(password)
            return bcrypt.checkpw(password, hash)
        except TypeError:
            # If the parameter hash is not encoded correctly, i.e a String was passed
            # a type error will be raised
            return False

    def getRole(self, role):
        # GetRole returns a role_id from the role parameter
        if str(role).isdigit():
            # If role is a digit, then it assumed that this is the role_id
            # Validation of role_id is done  automatically when inserting, so it is redundant to do so here
            return int(role)
        else:
            # If role is a string, then its role_id is found here, only if it exists
            self.cursor.execute(f"SELECT role_id FROM roles WHERE role_name = '{role}'")
            data = self.cursor.fetchall()

            if len(data) == 0 or len(data[0]) == 0 or data[0][0] is None:
                raise DatabaseError(f"Could not find role '{role}' in database")
            return data[0][0]

    def getId(self):
        # Finds the highest id in the staff table and returns the next available id
        self.cursor.execute("SELECT max(staff_id) FROM staff")
        data = self.cursor.fetchall()
        if len(data) == 0 or len(data[0]) == 0 or data[0][0] is None:
            return 1
        else:
            return data[0][0] + 1

    def addAdmin(self, first_name, last_name, username, password, role):
        # Create a new user to be inputted into the staff table
        try:
            role = self.getRole(role)
            hash = self.createHash(password)
            id = self.getId()
            self.cursor.execute(f"INSERT INTO staff VALUES(?,?,?,?,?,?)",
                                (id, first_name, last_name, username, hash, role))
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            raise DatabaseError(f"Could not add {username} to table -> " + str(e))

    def isAdmin(self, username, password):
        # Checks whether the username exists in the database and if the password is a match
        self.cursor.execute(f'''
                            SELECT password
                            FROM staff
                            WHERE lower(username) = '{username.lower()}'
                            ''')
        data = self.cursor.fetchall()
        if len(data) == 0 or len(data[0]) == 0:
            return False

        return self.confirmHash(password, data[0][0])

    def reset(self):
        # Another table used for testing, will be removed once a database is in place
        self.cursor.execute("DROP table staff")
        self.conn.commit()
        self.createTables()

    def close(self):
        # Terminate connection with database
        self.conn.close()

    def isUsernameUnique(self, username):
        # Check whether a username already exists in the database as usernames must be unique even though they
        # are not primary keys
        self.cursor.execute(f"SELECT 1 FROM staff WHERE lower(username) = '{username.lower()}' ")
        data = self.cursor.fetchall()
        if len(data) == 0:
            return True

        return data[0][0] != 1


class DatabaseError(Exception):
    # Class to wrap the different exceptions into one class
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
