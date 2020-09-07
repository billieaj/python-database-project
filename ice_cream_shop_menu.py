'''''''''''''''''''''''''''''''''''''''
Coffee Shop Database Menu (SQLite 3)
Billie Johnson
This code is to access a database, and to add, delete, update, and display the data that is within the database. It can also create and recreate tables within the database.

'''''''''''''''''''''''''''''''''''''''

import sqlite3

def create_table(database_name,table_name,sql): #Creates and recreates a table
    with sqlite3.connect(database_name) as db:
        cursor = db.cursor()
        cursor.execute("select name from sqlite_master where name=?",(table_name,))
        result = cursor.fetchall()
        keep_table = True
        if len(result) == 1:
            response = input("The table {0} already exists, do you wish to recreate it (yes/no): ".format(table_name))
            if response == "yes":
                keep_table = False
                print("The table {0} table will be recreated - all existing data will be lost".format(table_name))
                cursor.execute("drop table if exists {0}".format(table_name))
                db.commit()
            elif response == "no":
                print("The existing table was kept.")
            else:
                print("Invalid input.")
        else:
            keep_table = False
        if not keep_table:
            cursor.execute(sql)
            db.commit()

def create_product_table(): #Creates the Product table
    sql = """create table Product 
              (ProductID integer, 
              Name text, 
              Price real, 
              primary key(ProductID))"""
    create_table(database_name, "Product", sql)

def create_customer_table(): #Creates the Customer table
    sql = """create table Customer
             (CustomerID integer,
             FirstName text,
             LastName text,
             TelephoneNumber text,
             EmailAddress text,
             primary key(CustomerID))"""
    create_table(database_name, "Customer", sql)
    
def create_order_table(): #Creates the order (CustomerOrder) table
    sql = """create table CustomerOrder
             (OrderID integer,
             Date real,
             Time real,
             CustomerID integer,
             ProductID integer,
             Quantity integer,
             primary key(OrderID)
             foreign key(CustomerID) references Customer(CustomerID),
             foreign key(ProductID) references Product(ProductID))""" 
    create_table(database_name, "CustomerOrder", sql)

def query(sql,data): 
    with sqlite3.connect("ice_cream_shop.db") as db:
        cursor = db.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute(sql,data)
        db.commit()
        
def insert_product(values): #Inserts data into Product
    with sqlite3.connect("ice_cream_shop.db") as db:
        cursor = db.cursor()
        sql = "insert into Product (Name, Price) values (?,?)"
        query(sql,values)

def delete_product(product_id): #Deletes product data from Product
    with sqlite3.connect("ice_cream_shop.db") as db:
        cursor = db.cursor()
        sql = "delete from Product where Name=?"
        cursor.execute(sql,data)
        db.commit()
        
def update_product(data): #Updates product data in Product
    with sqlite3.connect("ice_cream_shop.db") as db:
        cursor= db.cursor()
        sql = "update Product set Name=?, Price=? where ProductID=?"
        cursor.execute(sql,data)
        db.commit()

def select_all_products(): #Selects all products from Product
    with sqlite3.connect("ice_cream_shop.db") as db:
        cursor = db.cursor()
        cursor.execute("select * from Product")
        products = cursor.fetchall()
        for item in products:
            print(item[0], item[1], item[2])
            
def select_product_id(product_name): #Selects a ProductID from Product using Name
    with sqlite3.connect("ice_cream_shop.db") as db:
        cursor = db.cursor()
        cursor.execute("select ProductID from Product where Name=?",(product_name,))
        product_id = cursor.fetchone()
        return product_id

def select_product_name(product_id): #Selects a Name from Product using ProductID
    with sqlite3.connect("ice_cream_shop.db") as db:
        cursor = db.cursor()
        cursor.execute("select Name from Product where ProductID=?",(product_id))
        product_name = cursor.fetchone()
        return product_name

def select_name_product_price(product_name): #Selects a Price from Product using Name
    with sqlite3.connect("ice_cream_shop.db") as db:
        cursor = db.cursor()
        cursor.execute("select Price from Product where Name=?",(product_name,))
        product_price = cursor.fetchone()
        return product_price

def select_id_product_price(product_id): #Selects a Price from Product using ProductID
    with sqlite3.connect("ice_cream_shop.db") as db:
        cursor = db.cursor()
        cursor.execute("select Price from Product where ProductID=?",(product_id))
        product_price = cursor.fetchone()
        return product_price

def product_menu(): #Prints out menu options for product menu
    print("Product Table Menu")
    print("1. (Re)Create Product Table")
    print("2. Add new product")
    print("3. Edit existing product")
    print("4. Delete existing product")
    print("5. Search for products")
    print("0. Exit")    

def product_controller():
    try:
        choice = "1"
        while choice != "0":
            product_menu()
            choice = input("Please select an option: ")
            if choice == "1": #Creates and recreates Product table
                if __name__ == "__main__":
                    database_name = "ice_cream_shop.db"
                    create_product_table()           
            elif choice == "2": #Adds new product to Product
                if __name__ == "__main__":
                    product_name = input("Please enter the name of the new product: ")
                    product_price = input("Please enter the price of {}: ".format(product_name))
                    product = ("{}".format(product_name),"{}".format(product_price))
                    insert_product(product)
                    print("Product added.")
            elif choice == "3": #Updates product data in Product
                if __name__ == "__main__":
                    select_all_products()
                    product_id = int(input("Please enter the id of the product to edit: "))
                    product_name = input("Please enter the updated name of the product: ")
                    product_price = input("Please enter the updated price of {}: ".format(product_name))
                    data = "{}".format(product_name), "{}".format(product_price), "{}".format(product_id)
                    update_product(data)
                    print("Product has been updated.")
            elif choice == "4": #Deletes a product from Product
                if __name__ == "__main__":
                    select_all_products()
                    product_id = int(input("Please enter the id of the product you want to delete: "))
                    delete_product(product_id)
                    print("Product has been deleted, unless the product was contained in an order.")
            elif choice == "5": #Searches for and displays product using product id or product name
                if __name__ == "__main__":
                    choice = input("Would you like to search by product id (id), or product name (name)? ")
                    if choice == "name": #Selects and displays product information using Name
                        product_name = input("Please enter the name of the product to search by: ")
                        product_id = select_product_id(product_name)
                        product_price = select_name_product_price(product_name)
                        print("ID: {0:5} Name: {1:20} Price: {2:5}".format(product_id, product_name, product_price))
                    if choice == "id": #Selects and displays product information using ProductID
                        product_id = input("Please enter the id of the product to search for: ")
                        product_name = select_product_name(product_id)
                        product_price = select_id_product_price(product_id)
                        print("ID: {0:5} Name: {1:20} Price: {2:5}".format(product_id, product_name, product_price))
            elif choice == "0": #Exits the product menu
                break
            else:
                print("Invalid input.")
    except:
        print("Invalid input.")
        
def insert_customer(values): #Inserts data into Customer
    with sqlite3.connect("ice_cream_shop.db") as db:
        cursor = db.cursor()
        sql = "insert into Customer (FirstName,LastName,TelephoneNumber,EmailAddress) values (?,?,?,?)"
        query(sql,values)

def update_customer(data): #Updates the customer data in Customer
    with sqlite3.connect("ice_cream_shop.db") as db:
        cursor= db.cursor()
        sql = "update Customer set FirstName=?, LastName=?, TelephoneNumber=?, EmailAddress=? where CustomerID=?"
        cursor.execute(sql,data)
        db.commit()

def select_all_customers(): #Selects all customers from Customer
    with sqlite3.connect("ice_cream_shop.db") as db:
        cursor = db.cursor()
        cursor.execute("select * from Customer")
        customers = cursor.fetchall()
        for customer in customers:
            print(customer[0], customer[1], customer[2])
    
def select_customer_id(customer_first_name, customer_last_name): #Selects a CustomerID from Customer using FirstName and LastName
    with sqlite3.connect("ice_cream_shop.db") as db:
        cursor = db.cursor()
        cursor.execute("select CustomerID from Customer where FirstName=? and LastName=?",((customer_first_name), (customer_last_name)))
        customer_id = cursor.fetchone()
        return customer_id
          
def select_customer_first_name(customer_id): #Selects a FirstName from Customer using CustomerID
    with sqlite3.connect("ice_cream_shop.db") as db:
        cursor = db.cursor()
        cursor.execute("select FirstName from Customer where CustomerID=?",(customer_id))
        customer_first_name = cursor.fetchone()
        return customer_first_name
        
def select_customer_last_name(customer_id): #Selects a LastName from Customer using CustomerID
    with sqlite3.connect("ice_cream_shop.db") as db:
        cursor = db.cursor()
        cursor.execute("select LastName from Customer where CustomerID=?",(customer_id))
        customer_last_name = cursor.fetchone()
        return customer_last_name
        
def select_name_customer_phone(customer_first_name, customer_last_name): #Selects a TelephoneNumber from Customer using FirstName and LastName
    with sqlite3.connect("ice_cream_shop.db") as db:
        cursor = db.cursor()
        cursor.execute("select TelephoneNumber from Customer where FirstName=? and LastName=?",((customer_first_name), (customer_last_name)))
        customer_phone = cursor.fetchone()
        return customer_phone
        
def select_id_customer_phone(customer_id): #Selects a TelephoneNumber from Customer using CustomerID
    with sqlite3.connect("ice_cream_shop.db") as db:
        cursor = db.cursor()
        cursor.execute("select TelephoneNumber from Customer where CustomerID=?",(customer_id))
        customer_phone = cursor.fetchone()
        return customer_phone

def select_name_customer_email(customer_first_name, customer_last_name): #Selects an EmailAddress from Customer using FirstName and LastName
    with sqlite3.connect("ice_cream_shop.db") as db:
        cursor = db.cursor()
        cursor.execute("select EmailAddress from Customer where FirstName=? and LastName=?",((customer_first_name), (customer_last_name)))
        customer_email = cursor.fetchone()
        return customer_email

def select_id_customer_email(customer_id): #Selects an EmailAddress from Customer using CustomerID
    with sqlite3.connect("ice_cream_shop.db") as db:
        cursor = db.cursor()
        cursor.execute("select EmailAddress from Customer where CustomerID=?",(customer_id))
        customer_email = cursor.fetchone()
        return customer_email
  
        #print("ID: {0:5} First Name: {1:15} Last Name: {2:15} Phone: {3:15} Email: {4:20}".format(result[0], result[1], result[2], result[3], result[4]))

def customer_menu(): #Prints out menu options for customer menu
    print("Customer Table Menu")
    print("1. (Re)Create Customer Table")
    print("2. Add Customer")
    print("3. Amend Customer Details")
    print("4. View Customer Details")
    print("0. Exit")
    
def customer_controller():
    try:
        choice = "1"
        while choice != "0":
            customer_menu()
            choice = input("Please select an option: ")
            if choice == "1": #Creates and recreates Customer table
                if __name__ == "__main__":
                    database_name = "ice_cream_shop.db"
                    create_customer_table()
            elif choice == "2": #Adds a new customer
                if __name__ == "__main__":
                    customer_first_name = input("Please enter the first name of the new customer: ")
                    customer_last_name = input("Please enter the last name of the new customer: ")
                    customer_telephone_number = input("Please enter the telephone number of the new customer: ")
                    customer_email_address = input("Please enter the email address of the new customer: ")
                    customer = ("{}".format(customer_first_name),"{}".format(customer_last_name),"{}".format(customer_telephone_number),"{}".format(customer_email_address))
                    insert_customer(customer)
                    print("Customer added.")
            elif choice == "3": #Updates customer data
                if __name__ == "__main__":
                    select_all_customers() #Prints a list of all customers to select from
                    customer_id = int(input("Please enter the id of the customer to edit: "))
                    customer_first_name = input("Please enter the updated first name of the customer: ")
                    customer_last_name = input("Please enter the updated last name of the customer: ")
                    customer_telephone_number = input("Please enter the updated telephone number of the customer: ")
                    customer_email_address = input("Please enter the updated email address of the customer: ")
                    data = ("{}".format(customer_first_name),"{}".format(customer_last_name),"{}".format(customer_telephone_number),"{}".format(customer_email_address),"{}".format(customer_id))
                    update_customer(data)
                    print("Customer has been amended.")
            elif choice == "4": #Searches for and displays customer information using either FirstName and LastName or CustomerID
                if __name__ == "__main__":
                    choice = input("Would you like to search by customer id (id), or customer name (name)? ")
                    if choice == "id": #Searches for and displays customer information using CustomerID
                        customer_id = input("Please enter the id of the customer to search by: ")
                        customer_first_name = select_customer_first_name(customer_id)
                        customer_last_name = select_customer_last_name(customer_id)
                        customer_phone = select_id_customer_phone(customer_id)
                        customer_email = select_id_customer_email(customer_id)
                        print("ID: {0:5} First Name: {1:20} Last Name: {2:20} Phone: {3:15} Email {4:20}".format(customer_id, customer_first_name, customer_last_name, customer_phone, customer_email))
                    if choice == "name": #Searches for and displays customer information using FirstName and LastName
                        customer_first_name = input("Please enter the first name of the customer to search for: ")
                        customer_last_name = input("Please enter the last name of the customer to search for: ")
                        customer_id = select_customer_id((customer_first_name), (customer_last_name))
                        customer_phone = select_name_customer_phone((customer_first_name), (customer_last_name))
                        customer_email = select_name_customer_email((customer_first_name), (customer_last_name))
                        print("ID: {0:5} First Name: {1:20} Last Name: {2:20} Phone: {3:15} Email {4:20}".format(customer_id, customer_first_name, customer_last_name, customer_phone, customer_email))
            elif choice == "0": #Exits customer menu
                break
            else: #If user enters an unexpected value, the program quits
                print("Invalid input.")
    except:
        print("Invalid input.")

def insert_order(values): #Inserts data into CustomerOrder
    with sqlite3.connect("ice_cream_shop.db") as db:
        cursor = db.cursor()
        sql = "insert into CustomerOrder (Date, Time, CustomerID, ProductID, Quantity) values (?,?,?,?,?)"
        query(sql,values)
        
def select_all_orders(): #Selects all orders from CustomerOrder
    with sqlite3.connect("ice_cream_shop.db") as db:
        cursor = db.cursor()
        cursor.execute("select * from CustomerOrder")
        orders = cursor.fetchall()
        for order in orders:
            print(order[0], order[1], order[2])

def select_customer_order(customer_first_name, customer_last_name): #Selects an order from CustomerOrder using FirstName and LastName from Customer
    with sqlite3.connect("ice_cream_shop.db") as db:
        cursor = db.cursor()
        cursor.execute("select * from CustomerOrder where CustomerID = (select CustomerID from Customer where FirstName=? and LastName=?)",((customer_first_name),(customer_last_name)))
        order = cursor.fetchall()
        for result in order:
            print("OrderID: {0:5} Date: {1:15} Time: {2:10} CustomerID: {3:5} ProductID: {4:5} Quantity: {5:10}".format(result[0], result[1], result[2], result[3], result[4], result[5]))
            
def select_product_order(product_name): #Selects an order from CustomerOrder using Name from Product
    with sqlite3.connect("ice_cream_shop.db") as db:
        cursor = db.cursor()
        cursor.execute("select * from CustomerOrder where ProductID = (select ProductID from Product where Name=?)",(product_name,))
        order = cursor.fetchall()
        for result in order:
            print("OrderID: {0:5} Date: {1:15} Time: {2:10} CustomerID: {3:5} ProductID: {4:5} Quantity: {5:10}".format(result[0], result[1], result[2], result[3], result[4], result[5]))       

def order_menu(): #Prints out menu options for order menu
    print("Order Table Menu")
    print("1. (Re)Create Order Table")
    print("2. Add Order")
    print("3. Search and View Order")
    print("0. Exit")
    
def order_controller():
    try:
        choice = "1"
        while choice != "0":
            order_menu()
            choice = input("Please select an option: ")
            if choice == "1": #Creates and recreates CustomerOrder table
                if __name__ == "__main__":
                    database_name = "ice_cream_shop.db"
                    create_order_table()
            elif choice == "2": #Adds a new order
                if __name__ == "__main__":
                    order_date = input("Please enter the date: ") 
                    order_time = input("Please enter the time: ") 
                    select_all_customers()
                    customer_id = int(input("Please enter the id of the customer: "))
                    select_all_products()
                    order_product = int(input("Please enter the product id of the product: "))
                    order_quantity = int(input("Please enter the quantity of the product: "))
                    customer_order = ("{}".format(order_date),"{}".format(order_time),"{}".format(customer_id),"{}".format(order_product),"{}".format(order_quantity)) 
                    insert_order(customer_order)
                    print("Order added.")
            elif choice == "3": #Searches for and displays order using either product name or customer name
                if __name__ == "__main__":
                    choice = input("Would you like to search by product (product), or customer name (name)? ")
                    if choice == "product": #Searches for and displays order using the product name
                        product_name = input("Please enter the name of the product to search by: ")
                        select_product_order(product_name)
                    if choice == "name": #Searches for and displays order using the customer name
                        customer_first_name = input("Please enter the first name of the customer to search by: ")
                        customer_last_name = input("Please enter the last name of the customer to search by: ")
                        select_customer_order((customer_first_name), (customer_last_name))                          
            elif choice == "0": #Exits order menu
                break
            else: #If user enters an unexpected value, program quits
                print("Invalid input.")
    except:
        print("Invalid input.")

def menu(): #Prints out menu options for general menu
    print("Ice Cream Shop Menu")
    print("1. (Re)Create Tables")
    print("2. Add Customer")
    print("3. Add Order")
    print("4. Open Customer Menu")
    print("5. Open Order Menu")
    print("6. Open Product Menu")
    print("0. Exit")
    
try:
    choice = "1"
    while choice != "0":
        menu()
        choice = input("Please select an option: ")
        if choice == "1": #Creates and recreates all tables
            if __name__ == "__main__":
                database_name = "ice_cream_shop.db"
                create_product_table()
                create_customer_table()
                create_order_table()
        elif choice == "2": #Adds a new customer directly from starting menu
            if __name__ == "__main__":
                customer_first_name = input("Please enter the first name of the new customer: ")
                customer_last_name = input("Please enter the last name of the new customer: ")
                customer_telephone_number = input("Please enter the telephone number of the new customer: ")
                customer_email_address = input("Please enter the email address of the new customer: ")
                customer = ("{}".format(customer_first_name),"{}".format(customer_last_name),"{}".format(customer_telephone_number),"{}".format(customer_email_address))
                insert_customer(customer)
                print("Customer added.")    
        elif choice == "3": #Adds new orders directly from starting menu
            if __name__ == "__main__":
                order_date = input("Please enter the date: ") 
                order_time = input("Please enter the time: ")
                select_all_customers()
                customer_id = int(input("Please enter the id of the customer: "))
                select_all_products()
                order_product = int(input("Please enter the product id of the product: "))
                order_quantity = int(input("Please enter the quantity of the product: "))
                customer_order = ("{}".format(order_date),"{}".format(order_time),"{}".format(customer_id),"{}".format(order_product),"{}".format(order_quantity))
                insert_order(customer_order)
                print("Order added.")
        elif choice == "4": #Accesses customer menu
            if __name__ == "__main__":
                database_name = "ice_cream_shop.db"
                customer_controller()
        elif choice == "5": #Accesses order menu
            if __name__ == "__main__":
                database_name = "ice_cream_shop.db"
                order_controller()
        elif choice == "6": #Accesses product menu
            if __name__ == "__main__":
                database_name = "ice_cream_shop.db"
                product_controller()
        elif choice == "0": #Exits program
            break
        else:
            print("Invalid input.")
except:
    print("Invalid input.")