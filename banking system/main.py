import sqlite3
import random
import re
from datetime import datetime

# Database Initialization
def initialize_db():
    conn = sqlite3.connect('banking_system.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        account_number TEXT UNIQUE,
                        dob TEXT,
                        city TEXT,
                        password TEXT,
                        balance REAL,
                        contact_number TEXT,
                        email TEXT,
                        address TEXT,
                        status TEXT DEFAULT 'Active'
                    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        account_number TEXT,
                        type TEXT,
                        amount REAL,
                        date TEXT
                    )''')
    conn.commit()
    conn.close()

# Validations
def validate_name(name):
    return bool(re.match(r'^[A-Za-z ]+$', name))

def validate_contact(contact):
    return bool(re.match(r'^\d{10}$', contact))

def validate_email(email):
    return bool(re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email))

def validate_password(password):
    return bool(re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password))

def validate_balance(balance):
    return balance >= 2000

# Account Number Generator
def generate_account_number():
    return ''.join([str(random.randint(0, 9)) for _ in range(10)])

# Add User
def add_user():
    name = input("Enter Name: ")
    if not validate_name(name):
        print("Invalid Name!")
        return

    dob = input("Enter Date of Birth (YYYY-MM-DD): ")
    city = input("Enter City: ")

    password = input("Enter Password: ")
    if not validate_password(password):
        print("Invalid Password! Password must be 8 characters with uppercase, lowercase, digit, and special character.")
        return

    balance = float(input("Enter Initial Balance: "))
    if not validate_balance(balance):
        print("Minimum balance should be 2000.")
        return

    contact_number = input("Enter Contact Number: ")
    if not validate_contact(contact_number):
        print("Invalid Contact Number!")
        return

    email = input("Enter Email: ")
    if not validate_email(email):
        print("Invalid Email!")
        return

    address = input("Enter Address: ")
    account_number = generate_account_number()

    conn = sqlite3.connect('banking_system.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (name, account_number, dob, city, password, balance, contact_number, email, address) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', 
                   (name, account_number, dob, city, password, balance, contact_number, email, address))
    conn.commit()
    conn.close()
    print(f"User Added Successfully! Account Number: {account_number}")

# Show Users
def show_users():
    conn = sqlite3.connect('banking_system.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()

    for user in users:
        print(f"Account Number: {user[2]}\nName: {user[1]}\nDOB: {user[3]}\nCity: {user[4]}\nBalance: {user[6]}\nContact: {user[7]}\nEmail: {user[8]}\nAddress: {user[9]}\nStatus: {user[10]}\n")

# Login
def login():
    account_number = input("Enter Account Number: ")
    password = input("Enter Password: ")

    conn = sqlite3.connect('banking_system.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE account_number = ? AND password = ?', (account_number, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        print(f"Welcome {user[1]}!\n")
        while True:
            print("1. Show Balance\n2. Show Transactions\n3. Credit Amount\n4. Debit Amount\n5. Transfer Amount\n6. Change Password\n7. Update Profile\n8. Logout")
            choice = int(input("Enter your choice: "))

            if choice == 1:
                print(f"Balance: {user[6]}")

            elif choice == 2:
                conn = sqlite3.connect('banking_system.db')
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM transactions WHERE account_number = ?', (account_number,))
                transactions = cursor.fetchall()
                conn.close()
                for transaction in transactions:
                    print(f"Type: {transaction[2]} Amount: {transaction[3]} Date: {transaction[4]}")

            elif choice == 3:
                amount = float(input("Enter amount to credit: "))
                conn = sqlite3.connect('banking_system.db')
                cursor = conn.cursor()
                cursor.execute('UPDATE users SET balance = balance + ? WHERE account_number = ?', (amount, account_number))
                cursor.execute('INSERT INTO transactions (account_number, type, amount, date) VALUES (?, ?, ?, ?)', (account_number, 'Credit', amount, datetime.now()))
                conn.commit()
                conn.close()
                print("Amount Credited Successfully!")

            elif choice == 8:
                print("Logged Out Successfully!")
                break
            else:
                print("Invalid Choice!")
    else:
        print("Invalid Credentials!")

# Main Menu
def main():
    initialize_db()
    while True:
        print("1. Add User\n2. Show Users\n3. Login\n4. Exit")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            add_user()
        elif choice == 2:
            show_users()
        elif choice == 3:
            login()
        elif choice == 4:
            print("Exiting Application.")
            break
        else:
            print("Invalid Choice!")

if __name__ == "__main__":
    main()
