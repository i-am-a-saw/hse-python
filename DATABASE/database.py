import tkinter as tk
import sqlite3
from tkinter import messagebox, ttk

USER = "User"
PASSWORD = "Super-SEcure"

class LoginPage(tk.Frame):

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        login_lb = tk.Label(self, text="Login")
        password_lb = tk.Label(self, text="Password")
        self.login = tk.Entry(self)
        self.password = tk.Entry(self, show='*')
        self.submit = tk.Button(self, text="Log in")

        self.submit.config(background="white",  font="TimesNewRoman")
        self.submit.config(command=self.login_command)
        self.login.bind('<Return>', self.login_command)
        self.password.bind('<Return>', self.login_command)

        self.login.insert(0, USER)
        self.password.insert(0, PASSWORD)

        login_lb.pack(anchor="s", ipadx=130)
        self.login.pack(anchor="s")
        password_lb.pack(anchor="s")
        self.password.pack(anchor="s")
        self.submit.pack(anchor="s")

    def login_command(self, *args, **kwargs):
        if self.login.get() == USER and self.password.get() == PASSWORD:
            self.forget()
            app = MainPage(self.master)
        else:
            messagebox.showerror(title="Error", message="Incorrect input!")

class MainPage:
    def __init__(self, master):
        self.master = master
        self.master.title("Beer Producers Database")
        self.master.geometry("1320x800")

        # Создание или подключение к базе данных
        self.conn = sqlite3.connect('beer_database.db')
        self.cursor = self.conn.cursor()

        style = ttk.Style()
        style.configure("Treeview", rowheight = 15)

        # Создание таблицы производителей, если она не существует
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Producers (
            producer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            country TEXT NOT NULL,
            total_amount INTEGER,
            UNIQUE(name, country)  -- Добавление уникального ограничения
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS BeerTypes (
            beer_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            alcohol_content REAL NOT NULL,
            producer_id INTEGER
        )
        ''')
       
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Bottles (
            bottle_id INTEGER PRIMARY KEY AUTOINCREMENT,
            beer_name TEXT,
            volume REAL NOT NULL,
            price REAL NOT NULL,
            producer_name TEXT
        )
        ''') 

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Sales (
            sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
            bottle_id INTEGER,
            beer_type_id REAL NOT NULL,
            cost INTEGER,
            date DATE
        )
        ''') 
        
        self.conn.commit()

        # Ввод данных о производителе
        self.f1 = tk.Frame(self.master, width = 100, height = 100, relief=tk.GROOVE, borderwidth=4)
        self.f1.grid(row=0, column=0)
        
        tk.Label(self.f1, text="Producer Name").grid(row=0, column=0)
        self.producer_name_entry = tk.Entry(self.f1)
        self.producer_name_entry.grid(row=0, column=1)

        tk.Label(self.f1, text="Country").grid(row=1, column=0)
        self.producer_country_entry = tk.Entry(self.f1)
        self.producer_country_entry.grid(row=1, column=1)

        tk.Button(self.f1, text="Add Producer", command=self.add_producer).grid(row=2, column=1)
        tk.Button(self.f1, text="Delete Producer", command=self.delete_producer).grid(row=8, column=1)

        # Таблица для отображения производителей
        self.columns1 = ("ID", "Name", "Country", "Total Price")
        self.tree1 = ttk.Treeview(self.f1, columns=self.columns1, show='headings')
        self.tree1.column("ID", width=50)
        self.tree1.heading("ID", text="ID")
        self.tree1.heading("Name", text="Name")
        self.tree1.heading("Country", text="Country")
        self.tree1.heading("Total Price", text="Total Price")
        self.tree1.grid(row=4, columnspan=2)

        # Поиск по имени производителя
        tk.Label(self.f1, text="Search producer:").grid(row=6, column = 0)
        self.search_producer_entry = tk.Entry(self.f1)
        self.search_producer_entry.grid(row=7, column = 0)
        tk.Button(self.f1, text="Search", command = self.search_producers).grid(row=8, column=0)

        # Вывод всей таблицы
        tk.Button(self.f1, text="Reset", command=self.load_producers).grid(row=6, column=1)
        tk.Button(self.f1, text="Clear All", command=self.clear_producers).grid(row=7, column=1)

        # Загрузка существующих производителей при запуске
        self.load_producers()

        # Ввод данных о виде пива
        self.f2 = tk.Frame(self.master, width = 100, height = 100, relief=tk.GROOVE, borderwidth=4)
        self.f2.grid(row=0, column=1)
        
        tk.Label(self.f2, text="Beer Name").grid(row=0, column=0)
        self.beer_name_entry = tk.Entry(self.f2)
        self.beer_name_entry.grid(row=0, column=1)

        tk.Label(self.f2, text="Alcohol Content").grid(row=1, column=0)
        self.beer_alcohol_entry = tk.Entry(self.f2)

        self.beer_alcohol_entry.grid(row=1, column=1)

        tk.Label(self.f2, text="Producer ID").grid(row=2, column=0)
        self.beer_producer_id_entry = tk.Entry(self.f2)
        self.beer_producer_id_entry.grid(row=2, column=1)

        tk.Button(self.f2, text="Add Beer Type", command=self.add_beer_type).grid(row=3, column=1)
        tk.Button(self.f2, text="Delete Beer Type", command=self.delete_beer_type).grid(row=5, column=1)

        tk.Button(self.f2, text="Clear All", command=self.clear_beer_types).grid(row=6, column=1)

        # Таблица для отображения видов пива
        self.columns2 = ("ID", "Beer Name", "Alcohol Content", "Producer ID")
        self.tree2 = ttk.Treeview(self.f2, columns=self.columns2, show='headings')
        self.tree2.column("ID", width=50)
        self.tree2.heading("ID", text="ID")
        self.tree2.heading("Beer Name", text="Beer Name")
        self.tree2.heading("Alcohol Content", text="Alcohol Content")
        self.tree2.heading("Producer ID", text="Producer ID")
        self.tree2.grid(row=4, columnspan=2)

        # Загрузка пива при запуске
        self.load_beer_types()

        # Ввод данных о бутылках
        self.f3 = tk.Frame(self.master, width = 100, height = 100, relief=tk.GROOVE, borderwidth=4)
        self.f3.grid(row=1, column=0)

        tk.Label(self.f3, text="Beer Name").grid(row=0, column=0)
        self.bottle_name_entry = tk.Entry(self.f3)
        self.bottle_name_entry.grid(row=0, column=1)

        tk.Label(self.f3, text="Volume").grid(row=1, column=0)
        self.volume_entry = tk.Entry(self.f3)
        self.volume_entry.grid(row=1, column=1)

        tk.Label(self.f3, text="Price").grid(row=2, column=0)
        self.price_entry = tk.Entry(self.f3)
        self.price_entry.grid(row=2, column=1)

        tk.Label(self.f3, text="Producer Name").grid(row=3, column=0)
        self.beer_prod_entry = tk.Entry(self.f3)
        self.beer_prod_entry.grid(row=3, column=1)

        tk.Button(self.f3, text="Add Bottle", command=self.add_bottle).grid(row=4, column=1, columnspan=2)
        tk.Button(self.f3, text="Delete Bottle", command=self.delete_bottle).grid(row=6, column=1)
        tk.Button(self.f3, text="Clear All", command=self.clear_bottles).grid(row=7, column=1)

        # Таблица для отображения бутылок
        self.columns3 = ("ID", "Name", "Volume", "Price", "Producer Name")
        self.tree3 = ttk.Treeview(self.f3, columns=self.columns3, show='headings')
        self.tree3.column("ID", width=50)
        self.tree3.heading("ID", text="ID")
        self.tree3.column("Name", width=140)
        self.tree3.heading("Name", text="Name")
        self.tree3.column("Volume", width=130)
        self.tree3.heading("Volume", text="Volume")
        self.tree3.column("Price", width=130)
        self.tree3.heading("Price", text="Price")
        self.tree3.heading("Producer Name", text="Producer Name")
        self.tree3.grid(row=5, columnspan=2)
    
        # Загрузка бутылок при запуске
        self.load_bottles()

        # Ввод данных о продажах
        self.f4 = tk.Frame(self.master, width = 100, height = 100, relief=tk.GROOVE, borderwidth=4)
        self.f4.grid(row=1, column=1)

        tk.Label(self.f4, text="Bottle ID").grid(row=0, column=0)
        self.bottle_id_entry = tk.Entry(self.f4)
        self.bottle_id_entry.grid(row=0, column=1)

        tk.Label(self.f4, text="Beer Type ID").grid(row=1, column=0)
        self.beer_type_entry = tk.Entry(self.f4)
        self.beer_type_entry.grid(row=1, column=1)

        tk.Label(self.f4, text="Cost").grid(row=2, column=0)
        self.cost_entry = tk.Entry(self.f4)
        self.cost_entry.grid(row=2, column=1)

        tk.Label(self.f4, text="Date").grid(row=3, column=0)
        self.date_entry = tk.Entry(self.f4)
        self.date_entry.grid(row=3, column=1)

        tk.Button(self.f4, text="Add Sale", command=self.add_sale).grid(row=4, column=1, columnspan=2)
        tk.Button(self.f4, text="Delete Sale", command=self.delete_sale).grid(row=6, column=1)
        tk.Button(self.f4, text="Clear All", command=self.clear_sales).grid(row=7, column=1)

        # Таблица для отображения продаж
        self.columns4 = ("ID", "Bottle ID", "Beer Type ID", "Cost", "Date")
        self.tree4 = ttk.Treeview(self.f4, columns=self.columns4, show='headings')
        self.tree4.column("ID", width=50)
        self.tree4.heading("ID", text="ID")
        self.tree4.column("Bottle ID", width=150)
        self.tree4.heading("Bottle ID", text="Bottle ID")
        self.tree4.column("Beer Type ID", width=140)
        self.tree4.heading("Beer Type ID", text="Beer Type ID")
        self.tree4.column("Cost", width=155)
        self.tree4.heading("Cost", text="Cost")
        self.tree4.column("Date", width=155)
        self.tree4.heading("Date", text="Date")
        
        self.tree4.grid(row=5, columnspan=2)
    
        # Загрузка продаж при запуске
        self.load_sales()
        

    def add_producer(self):
        name = self.producer_name_entry.get()
        country = self.producer_country_entry.get()
        
        if name and country:
            try:
                self.cursor.execute("INSERT INTO Producers (name, country, total_amount) VALUES (?, ?, ?)", (name, country, 0))
                self.conn.commit()
                messagebox.showinfo("Success", "Producer added successfully!")
                self.clear_entries()
                self.load_producers()
            except sqlite3.IntegrityError:
                messagebox.showwarning("Input Error", "This producer already exists.")
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields.")

    def delete_producer(self):
        selected_item = self.tree1.selection()
        if selected_item:
            producer_id = self.tree1.item(selected_item, 'values')[0]  # Получаем ID выбранного производителя
            self.cursor.execute("DELETE FROM Producers WHERE producer_id = ?", (producer_id,))
            self.conn.commit()
            messagebox.showinfo("Success", "Producer deleted successfully!")
            self.reset_ids()
            self.load_producers()
        else:
            messagebox.showwarning("Selection Error", "Please select a producer to delete.")

    def add_beer_type(self):
        name = self.beer_name_entry.get()
        alcohol_content = self.beer_alcohol_entry.get()
        producer_id = self.beer_producer_id_entry.get()

        if name and alcohol_content and producer_id:
            self.cursor.execute("INSERT INTO BeerTypes (name, alcohol_content, producer_id) VALUES (?, ?, ?)", 
                           (name, float(alcohol_content), int(producer_id)))
            self.conn.commit()
            messagebox.showinfo("Success", "Beer type added successfully!")
            self.clear_entries()
            self.load_beer_types()
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields.")

    def delete_beer_type(self):
        selected_item = self.tree2.selection()
        if selected_item:
            beer_type_id = self.tree2.item(selected_item, 'values')[0]  # Получаем ID выбранного вида пива
            self.cursor.execute("DELETE FROM BeerTypes WHERE beer_type_id = ?", (beer_type_id,))
            self.conn.commit()
            messagebox.showinfo("Success", "Beer deleted successfully!")
            self.reset_ids_beer_type()
            self.load_beer_types()
        else:
            messagebox.showwarning("Selection Error", "Please select a producer to delete.")

    def add_bottle(self):
        name = self.bottle_name_entry.get()
        volume = self.volume_entry.get()
        price = self.price_entry.get()
        producer_name = self.beer_prod_entry.get()
        print(self.beer_prod_entry.get())

        data = self.cursor.execute("SELECT * FROM Bottles")
        print(data.description)

        if name and volume and price and producer_name:
            self.cursor.execute("INSERT INTO Bottles (beer_name, volume, price, producer_name) VALUES (?, ?, ?, ?)", 
                           (name, volume, int(price), producer_name))
            self.cursor.execute('''
                UPDATE Producers
                SET total_amount = total_amount + ?
                WHERE name = ?
                ''', (int(price), producer_name))
            
            self.conn.commit()
            messagebox.showinfo("Success", "Bottle added successfully!")
            self.clear_entries()
            self.load_bottles()
            self.load_producers()
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields.")

    def delete_bottle(self):
        selected_item = self.tree3.selection()
        if selected_item:
            bottle_id = self.tree3.item(selected_item, 'values')[0]  # Получаем ID выбранного вида пива
            self.cursor.execute("DELETE FROM Bottles WHERE bottle_id = ?", (bottle_id,))
            self.conn.commit()
            messagebox.showinfo("Success", "Beer deleted successfully!")
            self.reset_ids_bottles()
            self.load_bottles()
        else:
            messagebox.showwarning("Selection Error", "Please select a producer to delete.")

    def add_sale(self):
        bottle_id = self.bottle_id_entry.get()
        beer_type_id = self.beer_type_entry.get()
        cost = self.cost_entry.get()
        date = self.date_entry.get()

        if bottle_id and beer_type_id and cost and date:
            self.cursor.execute("INSERT INTO Sales (bottle_id, beer_type_id, cost, date) VALUES (?, ?, ?, ?)", 
                           (bottle_id, beer_type_id, cost, date))
            self.conn.commit()
            messagebox.showinfo("Success", "Sale added successfully!")
            self.clear_entries()
            self.load_sales()
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields.")

    def delete_sale(self):
        selected_item = self.tree4.selection()
        if selected_item:
            sale_id = self.tree4.item(selected_item, 'values')[0]  # Получаем ID выбранной транзакции
            self.cursor.execute("DELETE FROM Sales WHERE sale_id = ?", (sale_id,))
            self.conn.commit()
            messagebox.showinfo("Success", "Sale deleted successfully!")
            self.reset_ids_sales()
            self.load_sales()
        else:
            messagebox.showwarning("Selection Error", "Please select a producer to delete.")

    def search_producers(self):
        self.cursor.execute("SELECT * FROM Producers WHERE name LIKE ?", ('%' + self.search_producer_entry.get() + '%',))
        
        results = self.cursor.fetchall()  # Получаем все результаты
        
        for row in self.tree1.get_children():
            self.tree1.delete(row)
        
        
        for row in results:
            self.tree1.insert("", tk.END, values=row)

    def load_producers(self):
        # Очистка списка перед загрузкой новых данных
        for row in self.tree1.get_children():
            self.tree1.delete(row)
        
        self.cursor.execute("SELECT * FROM Producers")
        for row in self.cursor.fetchall():
            self.tree1.insert("", tk.END, values=row)

    def load_beer_types(self):
        # Очистка списка перед загрузкой новых данных
        for row in self.tree2.get_children():
            self.tree2.delete(row)
        
        self.cursor.execute("SELECT * FROM BeerTypes")
        for row in self.cursor.fetchall():
            self.tree2.insert("", tk.END, values=row)

    def load_bottles(self):
        # Очистка списка перед загрузкой новых данных
        for row in self.tree3.get_children():
            self.tree3.delete(row)
        
        self.cursor.execute("SELECT * FROM Bottles")
        for row in self.cursor.fetchall():
            self.tree3.insert("", tk.END, values=row)

    def load_sales(self):
        # Очистка списка перед загрузкой новых данных
        for row in self.tree4.get_children():
            self.tree4.delete(row)
        
        self.cursor.execute("SELECT * FROM Sales")
        for row in self.cursor.fetchall():
            self.tree4.insert("", tk.END, values=row)

    def clear_entries(self):
        self.producer_name_entry.delete(0, tk.END)
        self.producer_country_entry.delete(0, tk.END)


    def close_connection(self):
        self.conn.close()

    def clear_producers(self):
        self.cursor.execute("DROP TABLE Producers")
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Producers (
            producer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            country TEXT NOT NULL,
            total_amount INTEGER
        )
        ''')
        self.conn.commit()
        self.load_producers()

    def clear_beer_types(self):
        self.cursor.execute("DROP TABLE BeerTypes")
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS BeerTypes (
            beer_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            alcohol_content REAL NOT NULL,
            producer_id INTEGER
        )
        ''')
        self.conn.commit()
        self.load_beer_types()

    def clear_bottles(self):
        self.cursor.execute("DROP TABLE Bottles")
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Bottles (
            bottle_id INTEGER PRIMARY KEY AUTOINCREMENT,
            beer_name TEXT,
            volume REAL NOT NULL,
            price REAL NOT NULL,
            producer_name TEXT
        )
        ''')
        self.conn.commit()
        self.load_bottles()

    def clear_sales(self):
        self.cursor.execute("DROP TABLE Sales")
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Sales (
            bottle_id INTEGER PRIMARY KEY AUTOINCREMENT,
            beer_name TEXT,
            volume REAL NOT NULL,
            price REAL NOT NULL,
            producer_name TEXT
        )
        ''')
        self.conn.commit()
        self.load_sales()
    
    def reset_ids(self):
        # Создаем временную таблицу с новыми идентификаторами
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS TempProducers (
            producer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            country TEXT NOT NULL,
            total_amount INTEGER,
            UNIQUE(name, country)  -- Добавление уникального ограничения
        )
        ''')
        
        # Копируем данные из старой таблицы в новую с новыми идентификаторами
        self.cursor.execute("INSERT INTO TempProducers (name, country, total_amount) SELECT name, country, total_amount FROM Producers")
        
        # Удаляем старую таблицу
        self.cursor.execute("DROP TABLE Producers")
        
        # Переименовываем временную таблицу в основную
        self.cursor.execute("ALTER TABLE TempProducers RENAME TO Producers")

        self.conn.commit()
        
    def reset_ids_beer_type(self):
        # Создаем временную таблицу с новыми идентификаторами
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS TempBeerTypes (
            beer_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            alcohol_content REAL NOT NULL,
            producer_id INTEGER
        )
        ''')
        
        # Копируем данные из старой таблицы в новую с новыми идентификаторами
        self.cursor.execute("INSERT INTO TempBeerTypes (name, alcohol_content, producer_id) SELECT name, alcohol_content, producer_id  FROM BeerTypes")
        
        # Удаляем старую таблицу
        self.cursor.execute("DROP TABLE BeerTypes")
        
        # Переименовываем временную таблицу в основную
        self.cursor.execute("ALTER TABLE TempBeerTypes RENAME TO BeerTypes")
        
        self.conn.commit()

    def reset_ids_bottles(self):
        # Создаем временную таблицу с новыми идентификаторами
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS TempBottles (
            bottle_id INTEGER PRIMARY KEY AUTOINCREMENT,
            beer_name TEXT,
            volume REAL NOT NULL,
            price REAL NOT NULL,
            producer_name TEXT
        )
        ''')
        
        # Копируем данные из старой таблицы в новую с новыми идентификаторами
        self.cursor.execute("INSERT INTO TempBottles (beer_name, volume, price, producer_name) SELECT beer_name, volume, price, producer_name FROM Bottles")
        
        # Удаляем старую таблицу
        self.cursor.execute("DROP TABLE Bottles")
        
        # Переименовываем временную таблицу в основную
        self.cursor.execute("ALTER TABLE TempBottles RENAME TO Bottles")
        
        self.conn.commit()

    def reset_ids_sales(self):
        # Создаем временную таблицу с новыми идентификаторами
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS TempSales (
            sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
            bottle_id INTEGER,
            beer_type_id REAL NOT NULL,
            cost INTEGER,
            date DATE
        )
        ''')
        
        # Копируем данные из старой таблицы в новую с новыми идентификаторами
        self.cursor.execute("INSERT INTO TempSales (bottle_id, beer_type_id, cost, date) SELECT bottle_id, beer_type_id, cost, date FROM Sales")
        
        # Удаляем старую таблицу
        self.cursor.execute("DROP TABLE Sales")
        
        # Переименовываем временную таблицу в основную
        self.cursor.execute("ALTER TABLE TempSales RENAME TO Sales")
        
        self.conn.commit()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("300x200")
    root.title("BEER DATABASE")

    login = LoginPage(root)
    #main = MainPage(root)
    login.grid(row=0,column=0)

    
    # Закрытие соединения с базой данных при выходе
    #root.protocol("WM_DELETE_WINDOW", lambda: [main.close_connection(), root.destroy()])
    
    # Запуск основного цикла приложения
    root.mainloop()
