import sqlite3


class Lines:
    Name = None
    Product = None
    Status = None

    def __init__(self, Name, Product, Status):
        self.Name = Name
        self.Product = Product
        self.Status = Status

    def InsertInLines(self):
        conn = sqlite3.connect('shoecraft.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Lines (Name, Product, Status) VALUES (?,?,?)",
            (self.Name, self.Product, self.Status))
        conn.commit()
        conn.close()