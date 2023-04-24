import datetime
import mysql.connector as sql
import maskpass


def makesqlconnection():
    return sql.connect(
        host="localhost", user="root", password="indian0660", database="online_store"
    )


def loggedUser(data):
    email = data[0][2]
    logginId = data[0][0]
    phoneNumber = data[0][3]
    while True:
        print("Welcome to the silk road online store, " + email)
        print("Select a option from below:")
        print("1. View products")
        print("2. View cart")
        print("3. View my order status")
        print("4. View my profile")
        print("5. Logout")
        wc = int(input(">> "))
        if wc == 1:
            try:
                conn = makesqlconnection()
                cur = conn.cursor()
                query = "SELECT product_id , product_name, product_qty , product_price , product_description , product_brand , product_avgRating FROM products GROUP BY product_id;"
                cur.execute(query)

                # Fetch the data from the database
                data = cur.fetchall()
                # print(data)
                print("------------------------------------------------------------")
                for item in data:
                    print("PRODUCT ID: ", item[0])
                    print("PRODUCT NAME: " + item[1])
                    print("QUANTITY: " + str(item[2]))
                    print("PRICE: " + str(item[3]))
                    print("DESCRIPTION: " + str(item[4]))
                    print("BRAND: " + str(item[5]))
                    print("AVERAGE RATING: " + str(item[6]))
                    print(
                        "------------------------------------------------------------"
                    )
                    print("\n")

                print("------------------------------------------------------------")
                print("1.Add a product to cart")
                print("2. Go back")

                ww = int(input(">> "))
                if ww == 1:
                    try:
                        product_id = int(input("Enter the product ID to add to cart: "))
                        quantity = int(input("Enter the quantity: "))
                        cur.execute(
                            f"SELECT product_qty FROM products WHERE product_id = {product_id};"
                        )
                        result = cur.fetchone()
                        print(result)
                        availableQty = result[0]
                        if availableQty < quantity:
                            print("Sorry, we don't have enough stock")
                        else:
                            cur.execute(
                                f"UPDATE products SET product_qty = product_qty - {quantity} WHERE product_id = {product_id};"
                            )

                            cur.execute(
                                f"SELECT total_items FROM cart WHERE cart_id = {logginId};"
                            )
                            result = cur.fetchone()
                            total_items = result[0]
                            cur.execute(
                                f"SELECT total_amount FROM cart WHERE cart_id = {logginId};"
                            )
                            result = cur.fetchone()
                            total_price = result[0]
                            cur.execute(
                                f"SELECT product_price FROM products WHERE product_id = {product_id};"
                            )
                            result = cur.fetchone()
                            product_price = result[0]
                            cur.execute(
                                f"UPDATE cart SET total_items = {total_items+quantity}, total_amount = {total_price+quantity*product_price} WHERE cart_id = {logginId};"
                            )
                            conn.commit()
                        print("Product added to cart successfully!")
                    except ValueError:
                        print("Invalid input! Please enter a valid integer.")
                    except sql.Error as e:
                        conn.rollback()
                        print(f"Error executing SQL query: {e}")

                elif ww == 2:
                    break

            except sql.Error as e:
                # Handle SQL error
                print(f"Error executing SQL query: {e}")

        if wc == 2:
            try:
                conn = makesqlconnection()
                cur = conn.cursor()
                cart_id = logginId
                query = f"SELECT cart_id, total_items, total_amount, offer_id FROM cart WHERE cart_id = '{cart_id}' GROUP BY cart_id;"
                cur.execute(query)

                # Fetch the data from the database
                data = cur.fetchone()
                if data:
                    print(
                        "------------------------------------------------------------"
                    )
                    print("Cart ID: " + str(data[0]))
                    print("Total Items: " + str(data[1]))
                    print("Total Amount: " + str(data[2]))
                    print("Offer ID: " + str(data[3]))
                    print(
                        "------------------------------------------------------------"
                    )
                    print("\n")
                    print("1. Checkout")
                    print("2. Go Back")
                    wd = int(input(">> "))
                    if wd == 1:
                        query = f"SELECT offer.offer_id, offer.promo_code, offer.max_discount, offer.min_amount FROM cart LEFT JOIN offer ON cart.offer_id = offer.offer_id WHERE cart.cart_id = {cart_id};"
                        cur.execute(query)
                        offer = cur.fetchone()
                        print("\n")
                        # print(offer)
                        if offer[0] != None:
                            print(
                                "------------------------------------------------------------"
                            )
                            print("Offer Applied!")
                            print(
                                "------------------------------------------------------------"
                            )
                            print("Offer ID: " + str(offer[0]))
                            print("Promo Code: " + str(offer[1]))
                            print("Min Amount: " + str(offer[2]))
                            print("Discount: " + str(offer[3]))
                            print(
                                "------------------------------------------------------------"
                            )
                            minAmount = offer[2]
                            discount = offer[3]
                            totalAmount = data[2]
                            if totalAmount >= minAmount:
                                totalAmount = totalAmount - discount
                                print(
                                    "Total Amount after discount: " + str(totalAmount)
                                )
                                query = f"UPDATE cart SET total_amount = {totalAmount} WHERE cart_id = {cart_id};"
                                cur.execute(query)
                                conn.commit()
                            else:
                                print(
                                    f"Add {minAmount- totalAmount} worth of items to apply the offer for a discount of {offer[3]}"
                                )
                        else:
                            print("Your cart currently has no promo-codes applied.")
                            print("Do you want to apply promo-code? (Y/N)")
                            applyOffer = input(">> ")
                            if applyOffer == ("Y" or "y"):
                                offerId = input(
                                    "Enter the promo-code to apply the offer: "
                                )
                                query = f"SELECT offer_id, promo_code, max_discount, min_amount FROM offer WHERE promo_code = '{offerId}';"
                                cur.execute(query)
                                offer = cur.fetchone()
                                # print(offer)
                                if offer[0]:
                                    print(
                                        "------------------------------------------------------------"
                                    )
                                    print("Offer Applied!")
                                    print(
                                        "------------------------------------------------------------"
                                    )
                                    print("Offer ID: " + str(offer[0]))
                                    print("Promo Code: " + str(offer[1]))
                                    print("Min Amount: " + str(offer[2]))
                                    print("Discount: " + str(offer[3]))
                                    print(
                                        "------------------------------------------------------------"
                                    )
                                    minAmount = offer[2]
                                    discount = offer[3]
                                    totalAmount = data[2]
                                    if totalAmount >= minAmount:
                                        totalAmount = totalAmount - discount
                                        print(
                                            "Total Amount after discount: "
                                            + str(totalAmount)
                                        )
                                        query = f"UPDATE cart SET total_amount = {totalAmount}, offer_id = {offer[0]} WHERE cart_id = {cart_id};"
                                        cur.execute(query)
                                        conn.commit()
                                    else:
                                        print(
                                            f"Add {minAmount- totalAmount} worth of items to apply the offer for a discount of {offer[3]}"
                                        )
                                else:
                                    print("Invalid promo-code!")
                            else:
                                print("Okay, no problem!")

                        # Update the order status in the orders table to "Dispatched"
                        paymentMode = input("Enter your preffered payment mode: ")
                        paymentDateTime = datetime.datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )

                        query = f"INSERT INTO payment (payment_id,payment_time_date,payment_mode,payment_details) VALUES ('{cart_id}','{paymentDateTime}','{paymentMode}','Approved');"
                        cur.execute(query)
                        conn.commit()
                        print("Your payment has been processed.")

                        # clear the cart
                        query = f"UPDATE cart SET total_items = 0, total_amount = 0, offer_id = NULL WHERE cart_id = {cart_id};"
                        cur.execute(query)
                        print("Your cart has been cleared.")

                        query = f"UPDATE orders SET order_status = 'Dispatched' WHERE order_id = {cart_id};"
                        cur.execute(query)
                        print("Your order has been dispatched.")

                        query = f"INSERT INTO orders (order_id,order_time_date, order_status, customer_id, payment_id, partner_id) VALUES ({cart_id},'2023-04-22', 'Processing', {cart_id}, {cart_id},75);"
                        cur.execute(query)

                        query = f"UPDATE delivery_partner SET order_id = {cart_id} WHERE order_id IS NULL LIMIT 1;"
                        cur.execute(query)
                        conn.commit()

                    elif wd == 2:
                        break
                    else:
                        print("Invalid input. Please enter 1 or 2")

                else:
                    print("No data found for the given cart ID")
            except Exception as e:
                print("Error: ", e)
        if wc == 3:
            try:
                conn = makesqlconnection()
                cur = conn.cursor()
                order_id = logginId
                query = f"SELECT order_id, order_status, customer_id FROM orders WHERE order_id = {order_id} GROUP BY order_id;"
                cur.execute(query)

                data = cur.fetchone()
                if data:
                    print(
                        "------------------------------------------------------------"
                    )
                    print("Order ID: " + str(data[0]))
                    print("Order Status: " + str(data[1]))
                    print("Customer ID: " + str(data[2]))

                    # trying to assign delivery partner if not already
                    query = f"UPDATE delivery_partner SET order_id = {order_id} WHERE order_id IS NULL LIMIT 1;"
                    cur.execute(query)
                    conn.commit()
                    # Fetch delivery partner name from the delivery_partner table for the same order_id
                    query = f"SELECT dp.partner_name,partner_description,partner_rating FROM delivery_partner dp JOIN orders o ON dp.order_id = o.order_id WHERE dp.order_id = '{order_id}'"
                    cur.execute(query)
                    temp = cur.fetchone()
                    if temp == None:
                        print("No delivery partner assigned yet.")
                        print("All delivery partners are busy.")
                        print(
                            "Please wait a moment before we can find a delivery partner for you"
                        )

                    else:
                        # print(temp)
                        dp_name = temp[0]
                        print("Delivery Partner Name: ", dp_name)
                        print("Delivery Partner Description: ", temp[1])
                        print("Delivery Partner rating: ", temp[2])
                        print(
                            "------------------------------------------------------------"
                        )

                    query = f"SELECT * FROM payment JOIN `orders` ON payment.payment_id = `orders`.payment_id WHERE orders.order_id = {order_id};"
                    cur.execute(query)
                    temp = cur.fetchone()
                    if temp == None:
                        print("No payment details found.")
                    else:
                        print("Payment ID: ", temp[0])
                        print("Payment Time: ", temp[1])
                        print("Payment Mode: ", temp[2])
                        print("Payment Details: ", temp[3])
                        print(
                            "------------------------------------------------------------"
                        )
                else:
                    print("No data found for the given cart ID")

            except sql.Error as e:
                print(f"Error executing SQL query: {e}")
        if wc == 4:
            conn = makesqlconnection()
            cur = conn.cursor()
            # print(data)
            print("Welcome to the silk road online store, " + data[0][1])
            print("Your current status: User")
            print("Your email id is: ", data[0][1])
            print("Your phone number is: ", data[0][3])
            print("Your address is :", data[0][4])

            print("Do you want to update any of the details?")
            ch = input("y/n >> ")
            if ch == "y":
                print("1. Update email id")
                print("2. Update phone number")
                print("3. Update address")
                print("4. Update password")
                chh = int(input())
                if chh == 1:
                    newEmail = input("Enter the new email: ")
                    query = f"UPDATE customer SET customer_emailid = '{newEmail}' WHERE customer_id = {logginId};"
                    cur.execute(query)
                    conn.commit()
                    print("Email id updated successfully!")
                elif chh == 2:
                    newPhone = input("Enter the new Phone Number: ")
                    query = f"UPDATE customer SET customer_emailid = '{newPhone}' WHERE customer_id = {logginId};"
                    cur.execute(query)
                    conn.commit()
                    print("Phone number updated successfully!")
                elif chh == 3:
                    newAdd = input("Enter the new Address: ")
                    query = f"UPDATE customer SET customer_address = '{newAdd}' WHERE customer_id = {logginId};"
                    cur.execute(query)
                    conn.commit()
                    print("Address updated successfully!")
                elif chh == 4:
                    newPass = input("Enter the new password: ")
                    query = f"UPDATE customer SET customer_psswd = '{newPass}' WHERE customer_id = {logginId};"
                    cur.execute(query)
                    conn.commit()
        if wc == 5:
            break


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
    print("6. Add a new delivery partner.")
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

    elif wc == 3:
        try:
            conn = makesqlconnection()
        except sql.Error as e:
            # Handle connection error
            print(f"Error connecting to the database: {e}")

        try:
            ID = int(input())
            cur = conn.cursor()
            query = f"SELECT * FROM customer WHERE customer_id = {ID};"
            cur.execute(query)

            # Fetch the data from the database
            data = cur.fetchall()
            print("------------------------------------------------------------")
            for item in data:
                print("CUSTOMER ID: " + str(item[0]))
                print("CUSTOMER EMAIL: " + item[2])
                print("CUSTOMER PHONE: " + str(item[3]))
                print("CUSTOMER ADDRESS: " + item[4])
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

    elif wc == 6:
        try:
            conn = makesqlconnection()
        except sql.Error as e:
            # Handle connection error
            print(f"Error connecting to the database: {e}")

        try:
            cur = conn.cursor()

            print("Please enter the following details to add a delivery partner:")
            partnerName = input("Enter the delivery partner name :")
            partnerEmail = input("Enter the delivery partner email :")
            partnerDescription = input("Enter the delivery partner description :")
            query = "INSERT INTO delivery_partner(partner_name, partner_email, partner_description) values (%s,%s,%s);"
            values = (partnerName, partnerEmail, partnerDescription)
            cur.execute(query, values)
            conn.commit()

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
            email = input("Enter your email id:")
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
                    # print(data)
                    loggedUser(data)

                else:
                    print("Incorrect login details. Try again.")

            except sql.Error as e:
                # Handle SQL error
                print(f"Error executing SQL query: {e}")

        elif wc == 2:
            print("Welcome to the registration screen")

            customer_emailid = input("Enter your email ID: ")
            customer_psswd = input("Enter your password: ")
            customer_phoneNumber = input("Enter your phone number: ")
            customer_address = input("Enter your address: ")

            # Connect to the database
            try:
                conn = makesqlconnection()
            except sql.Error as e:
                # Handle connection error
                print(f"Error connecting to the database: {e}")

            try:
                cur = conn.cursor()
                # Insert the data into the database
                cur.execute("SELECT* FROM customer;")
                data = cur.fetchall()
                customer_id = len(data) + 1 + 3
                cur.execute(
                    f"INSERT INTO cart (cart_id,total_items) VALUES ({customer_id},0);"
                )
                query = "INSERT INTO customer (customer_id,customer_psswd, customer_emailid, customer_phoneNumber, customer_address, cart_id) VALUES (%s, %s, %s, %s, %s,%s);"
                values = (
                    customer_id,
                    customer_psswd,
                    customer_emailid,
                    customer_phoneNumber,
                    customer_address,
                    customer_id,
                )
                cur.execute(query, values)
                # Commit the transaction
                conn.commit()

                # close the connection
                cur.close()
                conn.close()

                print("Registration successful.")

            except sql.Error as e:
                # Handle SQL error
                print(f"Error executing SQL query: {e}")

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
