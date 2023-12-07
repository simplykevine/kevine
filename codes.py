import re
import sqlite3

print("Welcome to Farmcode")

# Create a connection to the database
conn = sqlite3.connect('registration.db')
cursor = conn.cursor()

# Create a table to store registration information if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        email TEXT,
        password TEXT
    )
''')

# Create a table to store agronomists' information if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS agronomists (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        contact_number TEXT
    )
''')

# Create a table to store fertilizer information if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS fertilizers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        price REAL
    )
''')

# Add random agronomists to the table
agronomists = [('Prince RURANGWA', '+250 784 120 542'), ('Chol', '+211 921 619 229'), ('Gaius IRAKIZA', '+250 780 000 000'), ('Wengelawit Solomon', '+251 98 495 1144'), ('UMUTONI Kevine', '+250791507934')]
for agronomist in agronomists:
    cursor.execute('INSERT INTO agronomists (name, contact_number) VALUES (?, ?) ', agronomist)
conn.commit()

# Add random fertilizers to the table
fertilizers = [('Nitrogen', 10.99), ('Phosphorus', 8.99), ('Potassium', 12.99)]
for fertilizer in fertilizers:
    cursor.execute('INSERT INTO fertilizers (name, price) VALUES (?, ?)', fertilizer)
conn.commit()

class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

# Function to check if user exists
def check_user_exist(username):
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    return cursor.fetchone() is not None

# Registration
def is_valid_email(email):
    # Regular expression to check for a valid email format
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

def register():
    username = input("Enter your username: ")

    # Check if the user already exists
    if check_user_exist(username):
        print("User already exists. Try logging in instead.")
        return

    email = input("Enter your email address: ")

    # Check if the email is valid
    if not is_valid_email(email):
        print("Invalid email address format. Please enter a valid email.")
        return

    password = input("Enter your password: ")

    # Insert the user into the database
    cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, password))
    conn.commit()

    print("Registration successful! Welcome to the home.")
    return_to_menu()

# Login
def login():
    while True:
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        if username == '3' or password == '3':
            print("Going back to the main menu.")
            return

        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()

        if user is not None:
            print("Login successful! Welcome to the home.")
            while True:
                print("\nOptions:")
                print("1. Irrigate your crops")
                print("2. Use fertilizers")
                print("3. Go back to the main menu")

                choice = input("Enter your choice (1, 2, or 3): ")

                if choice == '1':
                    show_agronomists()
                    return_to_options()
                elif choice == '2':
                    show_fertilizers()
                    return_to_options()
                elif choice == '3':
                    print("Going back to the main menu.")
                    return
                else:
                    print("Invalid choice. Please enter 1, 2, or 3.")
            break

        else:
            print("Invalid username or password.")

# Function to display agronomists' information
def show_agronomists():
    cursor.execute('SELECT * FROM agronomists')
    agronomists = cursor.fetchall()

    if len(agronomists) > 0:
        print("Agronomists:")
        for agronomist in agronomists:
            print(f"Name: {agronomist[1]}, Contact Number: {agronomist[2]}")
    else:
        print("No agronomists found.")

# Function to display fertilizers' information
def show_fertilizers():
    cursor.execute('SELECT * FROM fertilizers')
    fertilizers = cursor.fetchall()

    if len(fertilizers) > 0:
        print("Fertilizers:")
        for fertilizer in fertilizers:
            print(f"Name: {fertilizer[1]}, Price: {fertilizer[2]}")
    else:
        print("No fertilizers found.")

# Function to return to options page after choosing option 1 or 2
def return_to_options():
    while True:
        choice = input("\nDo you want to go back to the options page? (Y/N): ")
        if choice.upper() == 'Y':
            break
        elif choice.upper() == 'N':
            return  # Return to the main menu

            # Close the database connection before exiting
            cursor.close()
            conn.close()

            exit()
        else:
            print("Invalid choice. Please enter Y or N.")

# Function to return to main menu after registration or login
def return_to_menu():
    while True:
        choice = input("\nDo you want to go back to the main menu? (Y/N): ")
        if choice.upper() == 'Y':
            break
        elif choice.upper() == 'N':
            print("Exiting the application. Goodbye!")

            # Close the database connection before exiting
            cursor.close()
            conn.close()

            exit()
        else:
            print("Invalid choice. Please enter Y or N.")

# Welcoming page
while True:
    print("\nOptions:")
    print("1. Register")
    print("2. Login")
    print("3. Exit")

    choice = input("Enter your choice (1, 2, or 3): ")

    if choice == '1':
        register()
    elif choice == '2':
        login()
    elif choice == '3':
        print("Exiting the application. Goodbye!")

        # Close the database connection before exiting
        cursor.close()
        conn.close()

        break
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")
