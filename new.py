import mysql.connector as sql
import maskpass
2
def makesqlconnection():
    return sql.connect(
        host="localhost", user="root", password="Anant@2004", database="online_store"
    )

def loggedUser(data):

    email = data[0][2]
    print("Welcome to the silk road online store, " + email)
    print("Select a option from below:")
    print("1. View products")
    print("2. View cart")
    print("3. View my orders")
    print("4. View my profile")
    print("0. Logout")
    wc = int(input(">> "))
    if wc == 1:
        try:
            conn = makesqlconnection()
        except sql.Error as e:
            # Handle connection error
            print(f"Error connecting to the database: {e}")

        try:
            cur = conn.cursor()
            query = "SELECT product_name, product_qty , product_price , product_description , product_brand , product_avgRating FROM products GROUP BY product_id;"
            cur.execute(query)

            # Fetch the data from the database
            data = cur.fetchall()
            print("------------------------------------------------------------")
            for item in data:
                print("PRODUCT NAME: " + item[0])
                print("QUANTITY: " + str(item[1]))
                print("PRICE: " + str(item[2]))
                print("DESCRIPTION: " + str(item[3]))
                print("BRAND: " + str(item[4]))
                print("AVERAGE RATING: " + str(item[5]))
                print("------------------------------------------------------------")

        except sql.Error as e:
            # Handle SQL error
            print(f"Error executing SQL query: {e}")
    
    if wc == 2:
        try:
            conn = makesqlconnection()
        except sql.Error as e:
            # Handle connection error
            print(f"Error connecting to the database: {e}")

        try:
            cur = conn.cursor()
            query = "SELECT cart_id, total_items , total_amount , final_amount , offer_id FROM cart GROUP BY cart_id;"
            cur.execute(query)

            # Fetch the data from the database
            data = cur.fetchall()
            print("------------------------------------------------------------")
            for item in data:
                print("Cart ID: " + str(item[0]))
                print("Total Items: " + str(item[1]))
                print("Total Amount: " + str(item[2]))
                print("Final Amount: " + str(item[3]))
                print("Offer ID: " + str(item[4]))
                print("------------------------------------------------------------")

        except sql.Error as e:
            # Handle SQL error
            print(f"Error executing SQL query: {e}")


def loggedAdmin(data):
    # print(data) [(1, 'admin', 'admin', 'admin')]
    print("Welcome to the silk road online store, " + data[0][1])
    print("You are successfully logged in as admin.")
    print("Select a option from below:")
    print("1. View product sales.")
    print("2. View category sales.")
    print("3. View customer details.")
    print("4. Add category.")
    print("5. Add product.")
    wc = int(input(">> "))
    if wc == 1:
        try:
            conn = makesqlconnection()
        except sql.Error as e:
            # Handle connection error
            print(f"Error connecting to the database: {e}")

        try:
            cur = conn.cursor()
            query = "SELECT product_name, SUM(product_qty) as total_quantity, SUM(product_qty * product_price) as total_revenue FROM products GROUP BY product_id;"
            cur.execute(query)

            # Fetch the data from the database
            data = cur.fetchall()
            print("------------------------------------------------------------")
            for item in data:
                print("PRODUCT: " + item[0])
                print("SOLD UNITS: " + str(item[1]))
                print("REVENUE GENERATED: " + str(item[2]))
                print("------------------------------------------------------------")

        except sql.Error as e:
            # Handle SQL error
            print(f"Error executing SQL query: {e}")

    elif wc == 2:
        try:
            conn = makesqlconnection()
        except sql.Error as e:
            # Handle connection error
            print(f"Error connecting to the database: {e}")

        try:
            cur = conn.cursor()
            query = "SELECT c.category_Name, SUM(p.product_qty * p.product_price) as revenue FROM category c JOIN products p ON c.category_id = p.category_id JOIN orders o ON o.customer_id = p.product_id GROUP BY c.category_Name;"
            cur.execute(query)

            # Fetch the data from the database
            data = cur.fetchall()
            print("------------------------------------------------------------")
            for item in data:
                print("CATEGORY NAME: " + item[0])
                print("REVENUE GENERATED: " + str(item[1]))
                print("------------------------------------------------------------")

        except sql.Error as e:
            # Handle SQL error
            print(f"Error executing SQL query: {e}")

    elif wc == 4:
        try:
            conn = makesqlconnection()
        except sql.Error as e:
            # Handle connection error
            print(f"Error connecting to the database: {e}")

        try:
            cur = conn.cursor()
            print("Please enter the following details to add a Category:")
            category_id = input("Category ID: ")
            category_Name = input("Category Name: ")
            admin_id = input("Admin ID: ")
            query = f"INSERT INTO category (category_Name) VALUES ({category_id},{category_Name},{admin_id})"
            cur.execute(query)

            # Commit the changes to the database
            conn.commit()

            print("Category added successfully.")

        except sql.Error as e:
            # Handle SQL error
            print(f"Error executing SQL query: {e}")


    elif wc == 5:
        try:
            conn = makesqlconnection()
        except sql.Error as e:
            # Handle connection error
            print(f"Error connecting to the database: {e}")

        try:
            cur = conn.cursor()
            print("Please enter the following details to add a product:")
            product_id = input("Product ID: ")
            product_name = input("Product Name: ")
            product_qty = input("Product Quantity: ")
            product_price = input("Product Price: ")
            product_description = input("Product Description: ")
            product_brand = input("Product Brand: ")
            product_avgRating = input("Product Average Rating: ")
            category_id = input("Category ID: ")
            query = f"INSERT INTO products (product_id, product_name, product_qty, product_price, product_description, product_brand, product_avgRating, category_id) VALUES ({product_id}, '{product_name}', {product_qty}, {product_price}, '{product_description}', '{product_brand}', {product_avgRating}, {category_id})"
            cur.execute(query)

            # Commit the changes to the database
            conn.commit()

            print("Product added successfully.")

        except sql.Error as e:
            # Handle SQL error
            print(f"Error executing SQL query: {e}")



def adminLogin():
    print("Welcome to admin login!")
    firstName = input("Enter your first name --> ")
    lastName = input("Enter your last name --> ")
    password = maskpass.askpass(mask="*")

    # Connect to the database
    try:
        conn = makesqlconnection()
    except sql.Error as e:
        # Handle connection error
        print(f"Error connecting to the database: {e}")

    try:
        cur = conn.cursor()
        # r = cur.execute("SELECT* from customer;")
        # print(r)
        # Insert the data into the database
        query = "SELECT* from admin where First_Name=%s and Last_Name=%s and Admin_Password=%s;"
        values = (firstName, lastName, password)
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
    while True:
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
            password = maskpass.askpass(mask="*")
            # Connect to the database
            try:
                conn = makesqlconnection()
            except sql.Error as e:
                # Handle connection error
                print(f"Error connecting to the database: {e}")

            try:
                cur = conn.cursor()
                # r = cur.execute("SELECT* from customer;")
                # print(r)
                # Insert the data into the database
                query = "SELECT* from customer where customer_emailid=%s and customer_psswd=%s;"
                values = (email, password)
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


if __name__ == "__main__":

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
