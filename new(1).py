import mysql.connector as sql
import maskpass
2
def makesqlconnection():
    return sql.connect(
        host="localhost", user="root", password="Anant@2004", database="newschema"
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
            cur = conn.cursor()
            cart_id = input("Enter user login ID: ")
            query = f"SELECT cart_id, total_items, total_amount, offer_id FROM cart WHERE cart_id = '{cart_id}' GROUP BY cart_id;"
            cur.execute(query)

            # Fetch the data from the database
            data = cur.fetchone()
            if data:
                print("------------------------------------------------------------")
                print("Cart ID: " + str(data[0]))
                print("Total Items: " + str(data[1]))
                print("Total Amount: " + str(data[2]))
                print("Offer ID: " + str(data[3]))
                print("------------------------------------------------------------")
                print("\n")
                print("1. Buy the products")
                print("2. Go Back")
                wd = int(input(">> "))
                if wd == 1:
                    # Update the order status in the orders table to "Dispatched"
                    query = f"UPDATE orders SET order_status = 'Dispatched' WHERE order_id = '{cart_id}';"
                    cur.execute(query)
                    conn.commit()
                    print("Order has been Dispatched")

                    # Update the order_id in delivery_partner table to the value stored in cart_id for the first row with a NULL order_id
                    query = f"UPDATE delivery_partner SET order_id = '{cart_id}' WHERE order_id IS NULL LIMIT 1;"
                    cur.execute(query)
                    conn.commit()

                elif wd == 2:
                    pass
                else:
                    print("Invalid input. Please enter 1 or 2")
            else:
                print("No data found for the given cart ID")
        except Exception as e:
            print("Error: ", e)
        # finally:
        #     cur.close()
        #     conn.close()


    if wc==3:
        try:
            conn = makesqlconnection()
            cur = conn.cursor()
            order_id = input("Enter user login ID: ")
            query = f"SELECT order_id, order_status, customer_id FROM orders WHERE order_id = '{order_id}' GROUP BY order_id;"
            cur.execute(query)

            data = cur.fetchone()
            if data:
                print("------------------------------------------------------------")
                print("Order ID: " + str(data[0]))
                print("Order Status: " + str(data[1]))
                print("Customer ID: " + str(data[2]))
                print("Delivery Partner ID: " + str(data[0]))
                print("Delivery Partner Name: ")
                
                # Fetch delivery partner name from the delivery_partner table for the same order_id
                query = f"SELECT dp.partner_name FROM delivery_partner dp JOIN orders o ON dp.order_id = o.order_id WHERE dp.order_id = '{order_id}'"
                cur.execute(query)
                dp_name = cur.fetchone()[0]  # Fetch the first column of the first row
                
                print(dp_name)
                print("------------------------------------------------------------")
            else:
                print("No data found for the given cart ID")

        except sql.Error as e:
            # Handle SQL error
            print(f"Error executing SQL query: {e}")
        # finally:
        #     cur.close()
        #     conn.close()




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
