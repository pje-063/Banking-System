import random
import json
from datetime import datetime

DATA_FILE = "accounts.json"

accounts = {}


def save_accounts():
    with open(DATA_FILE, "w") as file:
        json.dump(accounts, file, indent=4)


def load_accounts():
    global accounts

    try:
        with open(DATA_FILE, "r") as file:
            accounts = json.load(file)

    except FileNotFoundError:
        accounts = {}
# Generate a unique account number
def generate_account_number():
    while True:
        account_number = str(random.randint(100000, 999999))

        if account_number not in accounts:
            return account_number


# Create a new account
def create_account():
    print("\n========== CREATE ACCOUNT ==========")

    name = input("Enter your name: ")
    phone = input("Enter your phone number: ")
    pin = input("Create a 4-digit PIN: ")

    if len(pin) != 4 or not pin.isdigit():
        print("Invalid PIN. PIN must contain exactly 4 digits.")
        return

    account_number = generate_account_number()

    accounts[account_number] = {
        "name": name,
        "phone": phone,
        "pin": pin,
        "balance": 0.0,
        "transactions": []
    }

    save_accounts()

    print("\nAccount created successfully!")
    print("Your Account Number:", account_number)
    print("Please remember your account number and PIN.")


# Login
def login():
    print("\n========== LOGIN ==========")

    account_number = input("Enter Account Number: ")
    pin = input("Enter PIN: ")

    if account_number in accounts:
        if accounts[account_number]["pin"] == pin:
            print("\nLogin successful!")
            print("Welcome,", accounts[account_number]["name"])

            account_menu(account_number)
        else:
            print("Incorrect PIN.")
    else:
        print("Account not found.")


# Check balance
def check_balance(account_number):
    balance = accounts[account_number]["balance"]

    print("\n========== BALANCE ==========")
    print(f"Current Balance: ₹{balance:.2f}")


# Deposit money
def deposit(account_number):
    print("\n========== DEPOSIT ==========")

    try:
        amount = float(input("Enter amount to deposit: "))

        if amount <= 0:
            print("Amount must be greater than zero.")
            return

        accounts[account_number]["balance"] += amount

        transaction = (
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - "
            f"Deposited ₹{amount:.2f}"
        )

        accounts[account_number]["transactions"].append(transaction)
        save_accounts()
        print(f"₹{amount:.2f} deposited successfully.")

    except ValueError:
        print("Please enter a valid amount.")


# Withdraw money
def withdraw(account_number):
    print("\n========== WITHDRAW ==========")

    try:
        amount = float(input("Enter amount to withdraw: "))

        if amount <= 0:
            print("Amount must be greater than zero.")
            return

        balance = accounts[account_number]["balance"]

        if amount > balance:
            print("Insufficient balance.")
            return

        accounts[account_number]["balance"] -= amount

        transaction = (
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - "
            f"Withdrew ₹{amount:.2f}"
        )

        accounts[account_number]["transactions"].append(transaction)
        save_accounts()  
        print(f"₹{amount:.2f} withdrawn successfully.")

    except ValueError:
        print("Please enter a valid amount.")


# Transfer money
def transfer(account_number):
    print("\n========== TRANSFER ==========")

    receiver = input("Enter receiver account number: ")

    if receiver not in accounts:
        print("Receiver account not found.")
        return

    if receiver == account_number:
        print("You cannot transfer money to your own account.")
        return

    try:
        amount = float(input("Enter amount to transfer: "))

        if amount <= 0:
            print("Amount must be greater than zero.")
            return

        if amount > accounts[account_number]["balance"]:
            print("Insufficient balance.")
            return

        # Deduct money from sender
        accounts[account_number]["balance"] -= amount

        # Add money to receiver
        accounts[receiver]["balance"] += amount

        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        sender_transaction = (
            f"{time} - Transferred ₹{amount:.2f} "
            f"to Account {receiver}"
        )

        receiver_transaction = (
            f"{time} - Received ₹{amount:.2f} "
            f"from Account {account_number}"
        )

        accounts[account_number]["transactions"].append(
            sender_transaction
        )

        accounts[receiver]["transactions"].append(
            receiver_transaction
        )
        save_accounts()
        print(f"₹{amount:.2f} transferred successfully.")

    except ValueError:
        print("Please enter a valid amount.")


# Transaction history
def transaction_history(account_number):
    print("\n========== TRANSACTION HISTORY ==========")

    transactions = accounts[account_number]["transactions"]

    if len(transactions) == 0:
        print("No transactions found.")
        return

    for transaction in transactions:
        print(transaction)


# Change PIN
def change_pin(account_number):
    print("\n========== CHANGE PIN ==========")

    old_pin = input("Enter current PIN: ")

    if old_pin != accounts[account_number]["pin"]:
        print("Incorrect current PIN.")
        return

    new_pin = input("Enter new 4-digit PIN: ")
    confirm_pin = input("Confirm new PIN: ")

    if len(new_pin) != 4 or not new_pin.isdigit():
        print("PIN must contain exactly 4 digits.")
        return

    if new_pin != confirm_pin:
        print("PINs do not match.")
        return

    accounts[account_number]["pin"] = new_pin
    save_accounts()
    print("PIN changed successfully.")


# Account menu
def account_menu(account_number):

    while True:

        print("\n================================")
        print("         ACCOUNT MENU")
        print("================================")
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer")
        print("5. Transaction History")
        print("6. Change PIN")
        print("7. Logout")
        print("================================")

        choice = input("Enter your choice: ")

        if choice == "1":
            check_balance(account_number)

        elif choice == "2":
            deposit(account_number)

        elif choice == "3":
            withdraw(account_number)

        elif choice == "4":
            transfer(account_number)

        elif choice == "5":
            transaction_history(account_number)

        elif choice == "6":
            change_pin(account_number)

        elif choice == "7":
            print("\nLogged out successfully.")
            break

        else:
            print("Invalid choice. Please try again.")


# Main menu
def main():

    while True:

        print("\n================================")
        print("        BANKING SYSTEM")
        print("================================")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")
        print("================================")

        choice = input("Enter your choice: ")

        if choice == "1":
            create_account()

        elif choice == "2":
            login()

        elif choice == "3":
            print("\nThank you for using Banking System.")
            break

        else:
            print("Invalid choice. Please try again.")


# Start the program
if __name__ == "__main__":
    load_accounts()
    main()