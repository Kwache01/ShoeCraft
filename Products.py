import sqlite3


class Products:
    Name = None
    Description = None
    Stock = None

    def __init__(self, Name, Description, Stock):
        self.Name = Name
        self.Description = Description
        self.Stock = Stock

    def InsertInProducts(self):
        conn = sqlite3.connect('shoecraft.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Products (Name, Description, Stock) VALUES (?,?,?)",
            (self.Name, self.Description, self.Stock))
        conn.commit()
        conn.close()