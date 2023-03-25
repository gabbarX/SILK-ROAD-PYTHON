import mysql.connector as sql

def loggedUser(data):
    # print(data) [(105, 'bhuki123', 'bhuki@kutti.com', '4204204200', 'basti colony, gand nagri', None)]
    email = data[0][2]
    print("Welcome to the silk road online store, " + email)
    print("Select a option from below:")
    print("1. View products")
    print("2. View cart")
    print("3. View orders")
    print("4. Logout")

def loggedAdmin(data):
    # print(data) [(1, 'admin', 'admin', 'admin')]
    print("Welcome to the silk road online store, " + data[0][1])
    print("You are successfully logged in as admin.")
    print("Select a option from below:")
    print("1. View product sales.")
    print("2. View category sales.")
    print("2. View customer details.")
    print("3. Add category")
    print("4. Add product")
    wc = int(input(">> "))
    if wc == 1:
        try:
            conn = sql.connect(
                host="localhost",
                user="root",
                password="indian0660",
                database="online_store"
            )
        except sql.Error as e:
            # Handle connection error
            print(f"Error connecting to the database: {e}")

        try:
            cur = conn.cursor()
            # r = cur.execute("SELECT* from customer;")
            # print(r)
            # Insert the data into the database
            query = "SELECT product_name, SUM(product_qty) as total_quantity, SUM(product_qty * product_price) as total_revenue FROM products GROUP BY product_id;"
            # values = (firstName,lastName,password)
            cur.execute(query)

            # Fetch the data from the database
            data = cur.fetchall()
            # print(data)
            print("------------------------------------------------------------")
            for item in data:
                print("PRODUCT: "+item[0])
                print("SOLD UNITS: "+str(item[1]))
                print("REVENUE GENERATED: "+str(item[2]))
                print("------------------------------------------------------------")

        except sql.Error as e:
        # Handle SQL error
            print(f"Error executing SQL query: {e}")
    
    elif wc == 2:
        try:
            conn = sql.connect(
                host="localhost",
                user="root",
                password="indian0660",
                database="online_store"
            )
        except sql.Error as e:
            # Handle connection error
            print(f"Error connecting to the database: {e}")

        try:
            cur = conn.cursor()
            # r = cur.execute("SELECT* from customer;")
            # print(r)
            # Insert the data into the database
            query = "SELECT c.category_Name, SUM(p.product_qty * p.product_price) as revenue FROM category c JOIN products p ON c.category_id = p.category_id JOIN orders o ON o.customer_id = p.product_id GROUP BY c.category_Name;"
            # values = (firstName,lastName,password)
            cur.execute(query)

            # Fetch the data from the database
            data = cur.fetchall()
            # print(data)
            print("------------------------------------------------------------")
            for item in data:
                print("CATEGORY NAME: "+item[0])
                print("REVENUE GENERATED: "+str(item[1]))
                print("------------------------------------------------------------")

        except sql.Error as e:
        # Handle SQL error
            print(f"Error executing SQL query: {e}")
    


def adminLogin():
    print("Welcome to admin login!")
    firstName=input("Enter your first name --> ")
    lastName=input("Enter your last name --> ")
    password=input("Enter your password --> ")

    # Connect to the database
    try:
        conn = sql.connect(
            host="localhost",
            user="root",
            password="indian0660",
            database="online_store"
        )
    except sql.Error as e:
        # Handle connection error
        print(f"Error connecting to the database: {e}")

    try:
        cur = conn.cursor()
        # r = cur.execute("SELECT* from customer;")
        # print(r)
        # Insert the data into the database
        query = "SELECT* from admin where First_Name=%s and Last_Name=%s and Admin_Password=%s;"
        values = (firstName,lastName,password)
        cur.execute(query, values)

        # Fetch the data from the database
        data = cur.fetchall()

        # close the connection
        cur.close()
        conn.close()

        if data:
            loggedAdmin(data)
        else:
            print("Incorrect login details. Try again.")
    except sql.Error as e:
            # Handle SQL error
            print(f"Error executing SQL query: {e}")


def userLogin():
    while(True):
        print("Welcome to silk road user login!")
        print("Select a option from below:")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        wc = int(input(">> "))
        if wc == 1:
            print("Welcome to the login screen")
            print("Enter your email id:")
            email = input()
            print("Enter your password:")
            password = input()
            # Connect to the database
            try:
                conn = sql.connect(
                    host="localhost",
                    user="root",
                    password="indian0660",
                    database="online_store"
                )
            except sql.Error as e:
                # Handle connection error
                print(f"Error connecting to the database: {e}")

            try:
                cur = conn.cursor()
                # r = cur.execute("SELECT* from customer;")
                # print(r)
                # Insert the data into the database
                query = "SELECT* from customer where customer_emailid=%s and customer_psswd=%s;"
                values = (email,password)
                cur.execute(query, values)

                # Fetch the data from the database
                data = cur.fetchall()

                # close the connection
                cur.close()
                conn.close()

                if data:
                    print("You are successfully logged in.")
                    loggedUser(data)
                else:
                    print("Incorrect login details. Try again.")

            except sql.Error as e:
                # Handle SQL error
                print(f"Error executing SQL query: {e}")
            
        elif wc == 2:
            print("Welcome to the registration screen")
            print("HAhaa")

        elif wc == 3:
            print("Thank you for visiting us!")
            break

if __name__=='__main__':

    while True:

        print("Welcome to silk road online store!")
        print("Select a option from below:")
        print("1. User login")
        print("2. Admin login")
        print("3. Exit")
        wc = int(input(">> "))
        if wc == 1:
            userLogin()
        elif wc == 2:
            adminLogin()
        elif wc == 3:
            print("Thank you for visiting us!")
            break
        else:
            print("Invalid input. Try again.")