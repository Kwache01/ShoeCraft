from User import User
import sqlite3


class Managers(User):

    def __init__(self, Surname, Firstname, Middlename, AccessCode):
        super().__init__(Surname, Firstname, Middlename, AccessCode)

    def InsertInManagers(self):
        conn = sqlite3.connect('shoecraft.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Managers (Surname, Firstname, Middlename, AccessCode) VALUES (?,?,?,?)",
            (self.Surname, self.Firstname, self.Middlename, self.AccessCode))
        conn.commit()
        conn.close()