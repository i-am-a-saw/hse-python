import tkinter as tk
import os
from tkinter import messagebox, ttk
import mysql.connector
from mysql.connector import Error 

USER = "user"
PASSWORD = "T$^T4C&R657*V$8*9&CY"

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
        self.conn = self.create_connection_db("Beer")
        self.cursor = self.conn.cursor()

        self.cursor.callproc('create_producers')
        self.cursor.callproc('create_beer_types')
        self.cursor.callproc('create_bottles')
        self.cursor.callproc('create_sales')
        
        style = ttk.Style()
        style.configure("Treeview", rowheight = 15)

        # Ввод данных о производителе
        self.f1 = tk.Frame(self.master, width = 100, height = 100, relief=tk.GROOVE, borderwidth=4)
        self.f1.grid(row=0, column=0)

        tk.Label(self.f1, text = "Producers", font=("TimesNewRoman", 14)).grid(row=0, column=0, columnspan=3)
        tk.Label(self.f1, text="Producer Name").grid(row=1, column=0)
        self.producer_name_entry = tk.Entry(self.f1)
        self.producer_name_entry.grid(row=1, column=1)

        tk.Label(self.f1, text="Country").grid(row=2, column=0)
        self.producer_country_entry = tk.Entry(self.f1)
        self.producer_country_entry.grid(row=2, column=1)

        tk.Button(self.f1, text="Add Producer", command=self.add_producer).grid(row=3, column=1)
        tk.Button(self.f1, text="Delete Producer", command=self.delete_producer).grid(row=9, column=1)

        # Таблица для отображения производителей
        self.columns1 = ("ID", "Name", "Country", "Total Price")
        self.tree1 = ttk.Treeview(self.f1, columns=self.columns1, show='headings')
        self.tree1.column("ID", width=50)
        self.tree1.heading("ID", text="ID")
        self.tree1.heading("Name", text="Name")
        self.tree1.heading("Country", text="Country")
        self.tree1.heading("Total Price", text="Total Price")
        self.tree1.grid(row=5, columnspan=2)

        # Поиск по имени производителя
        tk.Label(self.f1, text="Search producer:").grid(row=6, column = 0)
        self.search_producer_entry = tk.Entry(self.f1)
        self.search_producer_entry.grid(row=7, column = 0)
        tk.Button(self.f1, text="Search", command = self.search_producers).place(x=120, y=319)

        # Вывод всей таблицы
        tk.Button(self.f1, text="Reset", command=self.load_producers).place(x=167, y=319)
        tk.Button(self.f1, text="Clear All", command=self.clear_producers).grid(row=7, column=1)

        # Загрузка существующих производителей при запуске
        self.load_producers()

        # Ввод данных о виде пива
        self.f2 = tk.Frame(self.master, width = 100, height = 100, relief=tk.GROOVE, borderwidth=4)
        self.f2.grid(row=0, column=1)

        tk.Label(self.f2, text = "Beer Tastes", font=("TimesNewRoman", 14)).grid(row=0, column=0, columnspan=3)
        tk.Label(self.f2, text="Beer Taste").grid(row=1, column=0)
        self.beer_name_entry = tk.Entry(self.f2)
        self.beer_name_entry.grid(row=1, column=1)

        tk.Label(self.f2, text="Alcohol Content").grid(row=2, column=0)
        self.beer_alcohol_entry = tk.Entry(self.f2)

        self.beer_alcohol_entry.grid(row=2, column=1)

        tk.Label(self.f2, text="Producer ID").grid(row=3, column=0)
        self.beer_producer_id_entry = tk.Entry(self.f2)
        self.beer_producer_id_entry.grid(row=3, column=1)

        tk.Button(self.f2, text="Add Beer Type", command=self.add_beer_type).grid(row=4, column=1)
        tk.Button(self.f2, text="Delete Beer Type", command=self.delete_beer_type).grid(row=7, column=1)
        
        tk.Button(self.f2, text="Clear All", command=self.clear_beer_types).grid(row=6, column=1)

        # Таблица для отображения видов пива
        self.columns2 = ("ID", "Beer Taste", "Alcohol Content", "Producer ID")
        self.tree2 = ttk.Treeview(self.f2, columns=self.columns2, show='headings')
        self.tree2.column("ID", width=50)
        self.tree2.heading("ID", text="ID")
        self.tree2.heading("Beer Taste", text="Beer Taste")
        self.tree2.heading("Alcohol Content", text="Alcohol Content")
        self.tree2.heading("Producer ID", text="Producer ID")
        self.tree2.grid(row=5, columnspan=2)

        # Поиск по имени производителя
        tk.Label(self.f2, text="Search beer type:").grid(row=6, column = 0)
        self.search_beer_type_entry = tk.Entry(self.f2)
        self.search_beer_type_entry.grid(row=7, column = 0)
        tk.Button(self.f2, text="Search", command = self.search_beer_type).place(x=227, y=319)
        tk.Button(self.f2, text="Reset", command=self.load_beer_types).place(x=275, y=319)

        # Загрузка пива при запуске
        self.load_beer_types()

        # Ввод данных о бутылках
        self.f3 = tk.Frame(self.master, width = 100, height = 100, relief=tk.GROOVE, borderwidth=4)
        self.f3.grid(row=1, column=0)

        tk.Label(self.f3, text = "Bottles", font=("TimesNewRoman", 14)).grid(row=0, column=0, columnspan=3)
        tk.Label(self.f3, text="Beer Name").grid(row=1, column=0)
        self.bottle_name_entry = tk.Entry(self.f3)
        self.bottle_name_entry.grid(row=1, column=1, columnspan=2)

        tk.Label(self.f3, text="Volume").grid(row=2, column=0)
        self.volume_entry = tk.Entry(self.f3)
        self.volume_entry.grid(row=2, column=1, columnspan=2)

        tk.Label(self.f3, text="Price").grid(row=3, column=0)
        self.price_entry = tk.Entry(self.f3)
        self.price_entry.grid(row=3, column=1, columnspan=2)

        tk.Label(self.f3, text="Producer Name").grid(row=4, column=0)
        self.beer_prod_entry = tk.Entry(self.f3)
        self.beer_prod_entry.grid(row=4, column=1, columnspan=2)

        tk.Button(self.f3, text="Add Bottle", command=self.add_bottle).grid(row=5, column=1, columnspan=2)
        tk.Button(self.f3, text="Delete Bottle", command=self.delete_bottle).grid(row=9, column=2)
        tk.Button(self.f3, text="Clear All", command=self.clear_bottles).grid(row=8, column=2)

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
        self.tree3.grid(row=6, columnspan=3)

        # Удаление по ID бутылки
        tk.Label(self.f3, text="Delete bottle by Beer Name:").grid(row=7, column = 1)
        self.search_bottle_for_deletion_entry = tk.Entry(self.f3)
        self.search_bottle_for_deletion_entry.grid(row=8, column = 1)
        tk.Button(self.f3, text="Delete", command = self.delete_bottle_by_beer_name).grid(row=9, column=1)

        # Поиск по названию бутылки
        tk.Label(self.f3, text="Search bottle:").grid(row=7, column = 0)
        self.search_bottle_name_entry = tk.Entry(self.f3)
        self.search_bottle_name_entry.grid(row=8, column = 0)
        tk.Button(self.f3, text="Search", command = self.search_bottles).place(x=68, y=361)
        tk.Button(self.f3, text="Reset", command=self.load_bottles).place(x=115, y=361)
    
        # Загрузка бутылок при запуске
        self.load_bottles()

        # Ввод данных о продажах
        self.f4 = tk.Frame(self.master, width = 100, height = 100, relief=tk.GROOVE, borderwidth=4)
        self.f4.grid(row=1, column=1)

        tk.Label(self.f4, text = "Sales", font=("TimesNewRoman", 14)).grid(row=0, column=0, columnspan=3)
        tk.Label(self.f4, text="Bottle ID").grid(row=1, column=0)
        self.bottle_id_entry = tk.Entry(self.f4)
        self.bottle_id_entry.grid(row=1, column=1, columnspan=2)

        tk.Label(self.f4, text="Beer Type ID").grid(row=2, column=0)
        self.beer_type_entry = tk.Entry(self.f4)
        self.beer_type_entry.grid(row=2, column=1, columnspan=2)

        tk.Label(self.f4, text="Cost").grid(row=3, column=0)
        self.cost_entry = tk.Entry(self.f4)
        self.cost_entry.grid(row=3, column=1, columnspan=2)

        tk.Label(self.f4, text="Date").grid(row=4, column=0)
        self.date_entry = tk.Entry(self.f4)
        self.date_entry.grid(row=4, column=1, columnspan=2)

        tk.Button(self.f4, text="Add Sale", command=self.add_sale).grid(row=5, column=1, columnspan=2)
        tk.Button(self.f4, text="Delete Sale", command=self.delete_sale).grid(row=9, column=2)
        tk.Button(self.f4, text="Clear All", command=self.clear_sales).grid(row=8, column=2)

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
        self.tree4.grid(row=6, columnspan=3)

        # Поиск по ID бутылки
        tk.Label(self.f4, text="Search sale:").grid(row=7, column = 0)
        self.search_sale_name_entry = tk.Entry(self.f4)
        self.search_sale_name_entry.grid(row=8, column = 0)
        tk.Button(self.f4, text="Search", command = self.search_sales).place(x=68, y=361)
        tk.Button(self.f4, text="Reset", command=self.load_sales).place(x=115, y=361)

        # Удаление по ID продажи
        tk.Label(self.f4, text="Delete sale by Bottle ID:").grid(row=7, column = 1)
        self.search_bottle_id_deletion_entry = tk.Entry(self.f4)
        self.search_bottle_id_deletion_entry.grid(row=8, column = 1)
        tk.Button(self.f4, text="Delete", command = self.delete_sale_by_bottle_id).grid(row=9, column=1)
    
        # Загрузка продаж при запуске
        self.load_sales()

        # Кнопка сноса датабазы
        tk.Button(self.master, text="Delete Database", command=self.annihilation).grid(row=2, column=1)

    def create_connection_db(self, db_name = None):
        connection_db = None
        try:
            connection_db = mysql.connector.connect(
                host = "localhost",
                user = "user",
                passwd = "T$^T4C&R657*V$8*9&CY",
                database = db_name
            )
            print("Подключение к MySQL успешно выполнено")
        except Error as db_connection_error:
            print("Возникла ошибка: ", db_connection_error)
        return connection_db        

    def add_producer(self):
        name = self.producer_name_entry.get()
        country = self.producer_country_entry.get()

        if name and country:
            try:
                self.cursor.callproc('AddProducer', (name, country, 0))
                self.clear_entries()
                self.load_producers()
                self.conn.commit()
            except:
                messagebox.showwarning("Input Error", "This producer already exists.")
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields.")

    def delete_producer(self):
        selected_item = self.tree1.selection()
        
        if selected_item:
            producer_name = self.tree1.item(selected_item, 'values')[1]  # Получаем ID выбранного производителя
            self.cursor.callproc('DeleteProducer', tuple((producer_name,)))
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
            try:
                self.cursor.callproc('AddBeerType', (name, alcohol_content, producer_id))
                self.clear_entries()
                self.load_beer_types()
                self.conn.commit()
            except:
                messagebox.showwarning("Input Error", "Incorrect data")
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields.")

    def delete_beer_type(self):
        selected_item = self.tree2.selection()
        if selected_item:
            beer_type_id = self.tree2.item(selected_item, 'values')[1]  # Получаем ID выбранного вида пива
            self.cursor.callproc('DeleteBeerType', tuple((beer_type_id,)))
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

        if name and volume and price and producer_name:
            self.cursor.callproc('AddBottle', (name, volume, price, producer_name))
            self.clear_entries()
            self.load_bottles()
            self.load_producers()
            self.conn.commit()
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields.")

    def delete_bottle(self):
        selected_item = self.tree3.selection()
        if selected_item:
            bottle_id = self.tree3.item(selected_item, 'values')[0]  # Получаем ID выбранного вида пива
            self.cursor.callproc('DeleteBottle', tuple((bottle_id,)))
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
           
            self.cursor.callproc('AddSale', (bottle_id, beer_type_id, cost, date))
            self.clear_entries()
            self.load_sales()
            self.conn.commit()
            
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields.")

    def delete_sale(self):
        selected_item = self.tree4.selection()
        if selected_item:
            sale_id = self.tree4.item(selected_item, 'values')[0]  # Получаем ID выбранной транзакции
            self.cursor.callproc('DeleteSale', tuple((sale_id,)))
            self.conn.commit()
            messagebox.showinfo("Success", "Sale deleted successfully!")
            self.reset_ids_sales()
            self.load_sales()
        else:
            messagebox.showwarning("Selection Error", "Please select a producer to delete.")

    def search_producers(self):
        self.cursor.callproc('SearchProducer', tuple((self.search_producer_entry.get(),)))

        for row in self.tree1.get_children():
            self.tree1.delete(row)

        for result in self.cursor.stored_results():
            for row in result.fetchall():
                self.tree1.insert("", tk.END, values=row)

        

    def search_beer_type(self):
        self.cursor.callproc('SearchBeerType', tuple((self.search_beer_type_entry.get(),)))

        for row in self.tree2.get_children():
            self.tree2.delete(row)
        
        for result in self.cursor.stored_results():
            for row in result.fetchall():
                self.tree2.insert("", tk.END, values=row)

    def search_bottles(self):
        self.cursor.callproc('SearchBottle', tuple((self.search_bottle_name_entry.get(),)))

        for row in self.tree3.get_children():
            self.tree3.delete(row)

        for result in self.cursor.stored_results():
            for row in result.fetchall():
                self.tree3.insert("", tk.END, values=row)

    def search_sales(self):
        self.cursor.callproc('SearchSale', tuple((self.search_sale_name_entry.get(),)))

        for row in self.tree4.get_children():
            self.tree4.delete(row)

        for result in self.cursor.stored_results():
            for row in result.fetchall():
                self.tree4.insert("", tk.END, values=row)

    def load_producers(self):
        self.cursor.callproc('LoadProducers')
        # Очистка списка перед загрузкой новых данных
        for row in self.tree1.get_children():
            self.tree1.delete(row)

        for result in self.cursor.stored_results():
            for row in result.fetchall():
                self.tree1.insert("", tk.END, values=row)

    def load_beer_types(self):
        self.cursor.callproc('LoadBeerTypes')
        # Очистка списка перед загрузкой новых данных
        for row in self.tree2.get_children():
            self.tree2.delete(row)

        for result in self.cursor.stored_results():
            for row in result.fetchall():
                self.tree2.insert("", tk.END, values=row)

    def load_bottles(self):
        self.cursor.callproc('LoadBottles')
        # Очистка списка перед загрузкой новых данных
        for row in self.tree3.get_children():
            self.tree3.delete(row)

        for result in self.cursor.stored_results():
            for row in result.fetchall():
                self.tree3.insert("", tk.END, values=row)

    def load_sales(self):
        self.cursor.callproc('LoadSales')
        # Очистка списка перед загрузкой новых данных
        for row in self.tree4.get_children():
            self.tree4.delete(row)

        for result in self.cursor.stored_results():
            for row in result.fetchall():
                self.tree4.insert("", tk.END, values=row)

    def clear_entries(self):
        self.producer_name_entry.delete(0, tk.END)
        self.producer_country_entry.delete(0, tk.END)

    def delete_bottle_by_beer_name(self):
        delete_id = self.search_bottle_for_deletion_entry.get()
        
        try:
            # Удаление записи из таблицы njxy
            self.cursor.callproc('DeleteBottleName', tuple((delete_id,)))
                
                # Проверка, сколько строк было удалено
            if self.cursor.rowcount > 0:
                print(f"Удалено {self.cursor.rowcount} запись(ей) с beer_name = {delete_id}.")
            else:
                print(f"Запись с beer_name = {delete_id} не найдена.")
                
                # Сохранение изменений
            self.conn.commit()
            self.reset_ids_bottles()
            self.load_bottles()
        except:
            print(f"Ошибка при удалении записи")

    def delete_sale_by_bottle_id(self):
        delete_id = self.search_bottle_id_deletion_entry.get()
        
        try:
            # Удаление записи из таблицы Sales
            self.cursor.callproc('DeleteSaleID', tuple((delete_id,)))
            
            # Проверка, сколько строк было удалено
            if self.cursor.rowcount > 0:
                print(f"Удалено {self.cursor.rowcount} запись(ей) с bottle_id = {delete_id}.")
            else:
                print(f"Запись с bottle_id = {delete_id} не найдена.")
            
            # Сохранение изменений
            self.conn.commit()
            self.reset_ids_sales()
            self.load_sales()
        except:
            print(f"Ошибка при удалении записи: {e}")

    def close_connection(self):
        self.conn.close()

    def clear_producers(self):
        self.cursor.callproc('ClearProducers')
        self.conn.commit()
        self.load_producers()

    def clear_beer_types(self):
        self.cursor.callproc('ClearBeerTypes')
        self.conn.commit()
        self.load_beer_types()

    def clear_bottles(self):
        self.cursor.callproc('ClearBottles')
        self.conn.commit()
        self.load_bottles()

    def clear_sales(self):
        self.cursor.callproc('ClearSales')
        self.conn.commit()
        self.load_sales()
    
    def reset_ids(self):
        self.cursor.callproc('ResetIDsProducers')

    def reset_ids_beer_type(self):
        self.cursor.callproc('ResetIDsBeerTypes')    

    def reset_ids_bottles(self):
        self.cursor.callproc('ResetIDsBottles')

    def reset_ids_sales(self):
        self.cursor.callproc('ResetIDsSales')

    def annihilation(self):
        if messagebox.askyesno(title="Confirmation", message="Do you want to delete the database?"):
            self.close_connection()
            try:
                os.remove("C:\\Users\\aleks\\Desktop\\beer_database.db")
            except:
                pass
            for row in self.tree1.get_children():
                 self.tree1.delete(row)
            for row in self.tree2.get_children():
                self.tree2.delete(row)
            for row in self.tree3.get_children():
                self.tree3.delete(row)
            for row in self.tree4.get_children():
                self.tree4.delete(row)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("300x200")
    root.title("BEER DATABASE")
    login = LoginPage(root)
    login.grid(row=0,column=0)
    root.mainloop()
