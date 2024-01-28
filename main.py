import sqlite3
from tabulate import tabulate
from itertools import chain
from Managers import Managers
from Lines import Lines
from Products import Products
import string


def CreateDatabase():
    conn = sqlite3.connect('shoecraft.db')
    cursor = conn.cursor()

    cursor.execute('''
                CREATE TABLE IF NOT EXISTS Admins(
                    Id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Surname TEXT NOT NULL,
                    Firstname TEXT NOT NULL,
                    Middlename TEXT,
                    AccessCode INTEGER NOT NULL
                )
            ''')

    cursor.execute('''
                CREATE TABLE IF NOT EXISTS Managers(
                    Id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Surname TEXT NOT NULL,
                    Firstname TEXT NOT NULL,
                    Middlename TEXT,
                    AccessCode INTEGER NOT NULL
                )
            ''')

    cursor.execute('''
                CREATE TABLE IF NOT EXISTS Products(
                    Id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Name TEXT NOT NULL,
                    Description TEXT,
                    Stock INTEGER NOT NULL
                )
            ''')

    cursor.execute('''
                CREATE TABLE IF NOT EXISTS Lines(
                    Id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Name TEXT NOT NULL,
                    Product INTEGER,
                    Status TEXT NOT NULL,
                    FOREIGN KEY (Product) REFERENCES Products(Id)
                )
            ''')

    conn.commit()
    conn.close()


def ViewTable(NameTable):
    conn = sqlite3.connect('shoecraft.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {NameTable}")
    rows = cursor.fetchall()
    print(tabulate(rows, headers=[i[0] for i in cursor.description]))
    conn.commit()
    conn.close()


def EditTable(NameTable):
    a = input("Выберите действие над таблицей"
              "\n1. Удаление"
              "\n2. Обновление"
              "\nВаш ответ:")
    match a:
        case "1":
            print("Удаление данных")
            while True:
                ViewTable(NameTable)
                conn = sqlite3.connect('shoecraft.db')
                cursor = conn.cursor()
                b = input("Введите ID для удаления:")
                cursor.execute(f"DELETE FROM {NameTable} WHERE Id = {b}")
                conn.commit()
                conn.close()
                print("Успешно удалено")
                c = input("Хотите продолжить? Да или Нет")
                if c == "Да":
                    continue
                else:
                    break

        case "2":
            print("Обновление данных")
            while True:
                ViewTable(NameTable)
                conn = sqlite3.connect('shoecraft.db')
                cursor = conn.cursor()
                cursor.execute(f"PRAGMA table_info({NameTable})")
                columns_data = cursor.fetchall()
                columns = [column[1] for column in columns_data]
                while True:
                    c = input("Выберите колонку для обновления:")
                    if c in columns:
                        id = input("Выберите идентификатор:")
                        new = input("Введите новое значение:")
                        sql_update_query = f"""Update {NameTable} set {c} = ? where Id = ?"""
                        data = (new, id)
                        cursor.execute(sql_update_query, data)

                        conn.commit()
                        conn.close()
                        break
                    else:
                        print("Колонка не найдена!")

                c = input("Хотите продолжить? Да или Нет")
                if c == "Да":
                    continue
                else:
                    break

        case _:
            print("Действие не найдено!")


def AddManager():
    Surname = NonDigit(input("Введите фамилию менеджера:"))
    Firstname = NonDigit(input("Введите имя менеджера:"))
    Middlename = NonDigit(input("Введите отчество менеджера:"))
    while True:
        AccessCode = input("Введите уникальный код менеджера:")
        check = AccessCode.isdigit()
        if check:
            break
        else:
            continue


    manager = Managers(Surname, Firstname, Middlename, AccessCode)
    manager.InsertInManagers()


def AddLine():
    Name = NonDigit(input("Введите наименование производственной линии:"))
    while True:
        Product = input("Введите ID продукта:")
        if Product.isdigit():
            break
        else:
            continue
    Status = input("Введите статус производственной линии:")

    line = Lines(Name, Product, Status)
    line.InsertInLines()


def AddProduct():
    Name = NonDigit(input("Введите наименование продукта:"))
    Description = input("Введите описание продукта:")
    while True:
        Stock = input("Введите количество продукта:")
        if Stock.isdigit():
            break
        else:
            continue

    product = Products(Name, Description, Stock)
    product.InsertInProducts()


def Authorize(Table):
    conn = sqlite3.connect('shoecraft.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT Surname FROM {Table}")
    login = list(chain.from_iterable(cursor.fetchall()))
    while True:
        user_login = input("Введите свой логин:")
        if user_login in login:
            cursor.execute(f"SELECT AccessCode FROM {Table}")
            codes = list(chain.from_iterable(cursor.fetchall()))
            while True:
                code = int((input("Введите код доступа:")))
                if code in codes:
                    cursor.execute(f"SELECT Firstname, Middlename FROM {Table} WHERE AccessCode = {code}")
                    fullName = cursor.fetchall()
                    fullName = ' '.join([idx for tup in fullName for idx in tup])
                    print(f"Здравствуйте, {fullName}. Добро пожаловать в базу данных!")
                    break
                else:
                    print("Неверный код доступа")
            break
        else:
            print("Сотрудник не найден в базе данных")


def NonDigit(string):
    while True:
        while True:
            if any(char.isdigit() for char in string):
                string = input("Некорректный ввод!\nВведите снова:")
            else:
                break

        return string


if __name__ == '__main__':
    CreateDatabase()
    while True:
        print("Обувная фабрика Shoe Craft. Отдел производства.")
        user = input("Кто вы?"
                     "\n1. Менеджер"
                     "\n2. Админ"
                     "\n3. Выйти из БД"
                     "\nВаш ответ:")

        if user == '1':
            print("Добро пожаловать! Для подтверждения уровня доступа введите свой логин и ключ доступа")
            Authorize("Managers")
            print("Выберите дальнейшие действия")
            while True:
                inp = input("1. Просмотр базы данных"
                            "\n2. Редактирование базы данных"
                            "\n3. Добавить продукт"
                            "\n4. Добавить производственную линию"
                            "\nВаш ответ:")

                match inp:
                    case '1':
                        while True:
                            NameTable = None
                            table = input("Выберите таблицу для просмотра"
                                          "\n1. Производственные линии"
                                          "\n2. Продукты"
                                          "\nВаш ответ:")
                            if table == '1':
                                NameTable = "Lines"
                            elif table == '2':
                                NameTable = "Products"
                            ViewTable(NameTable)
                            a = input("Выйти в меню? Да/Нет - ")
                            if a == "Да":
                                break
                            else:
                                continue
                    case '2':
                        while True:
                            NameTable = None
                            table = input("Выберите таблицу для редактирования"
                                          "\n1. Производственные линии"
                                          "\n2. Продукты"
                                          "\nВаш ответ:")
                            if table == '1':
                                NameTable = "Lines"
                            elif table == '2':
                                NameTable = "Products"
                            EditTable(NameTable)
                            a = input("Выйти в меню? Да/Нет - ")
                            if a == "Да":
                                break
                            else:
                                continue
                    case '3':
                        while True:
                            AddProduct()
                            a = input("Выйти в меню? Да/Нет - ")
                            if a == "Да":
                                break
                            else:
                                continue
                    case '4':
                        while True:
                            AddLine()
                            a = input("Выйти в меню? Да/Нет - ")
                            if a == "Да":
                                break
                            else:
                                continue

                    case _:
                        print("Действие не найдено")

        elif user == '2':
            Authorize("Admins")
            while True:
                vib = input("Выберите действие:"
                            "\n1. Добавить менеджера"
                            "\n2. Редактировать таблицу менеджеров"
                            "\nВаш выбор:")

                if vib == '1':
                    AddManager()
                elif vib == "2":
                    EditTable('Managers')
                else:
                    print("Действие не найдено!")

                a = input("Выйти в меню? Да/Нет - ")
                if a == "Да":
                    break
                else:
                    continue

        elif user == "3":
            break

        else:
            print("Уровень доступа не найден!")