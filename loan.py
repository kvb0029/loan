import json
import datetime

# File to store customer and loan data
DATA_FILE = "loan_data.json"

# Load data from file
def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save data to file
def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Add a new customer
def add_customer():
    data = load_data()
    customer_id = input("Enter Customer ID: ")
    if customer_id in data:
        print("Customer ID already exists.")
        return
    name = input("Enter Customer Name: ")
    data[customer_id] = {"name": name, "loans": []}
    save_data(data)
    print("Customer added successfully.")

# Add a loan to a customer
def add_loan():
    data = load_data()
    customer_id = input("Enter Customer ID: ")
    if customer_id not in data:
        print("Customer ID not found.")
        return
    amount = float(input("Enter Loan Amount: "))
    interest_rate = float(input("Enter Interest Rate (in %): "))
    duration = int(input("Enter Loan Duration (in months): "))
    start_date = datetime.datetime.now().strftime("%Y-%m-%d")

    loan = {
        "amount": amount,
        "interest_rate": interest_rate,
        "duration": duration,
        "start_date": start_date,
        "payments": []
    }

    data[customer_id]["loans"].append(loan)
    save_data(data)
    print("Loan added successfully.")

# Make a payment
def make_payment():
    data = load_data()
    customer_id = input("Enter Customer ID: ")
    if customer_id not in data:
        print("Customer ID not found.")
        return

    loans = data[customer_id]["loans"]
    if not loans:
        print("No active loans found for this customer.")
        return

    print("Active Loans:")
    for i, loan in enumerate(loans):
        print(f"{i + 1}. Amount: {loan['amount']}, Start Date: {loan['start_date']}")

    loan_index = int(input("Select Loan Number: ")) - 1
    if loan_index < 0 or loan_index >= len(loans):
        print("Invalid loan selection.")
        return

    amount = float(input("Enter Payment Amount: "))
    loans[loan_index]["payments"].append({"date": datetime.datetime.now().strftime("%Y-%m-%d"), "amount": amount})
    save_data(data)
    print("Payment recorded successfully.")

# Calculate Outstanding Balance
def calculate_balance(customer_id, loan):
    total_paid = sum(payment["amount"] for payment in loan["payments"])
    total_interest = loan["amount"] * (loan["interest_rate"] / 100) * (loan["duration"] / 12)
    return loan["amount"] + total_interest - total_paid

# View customer details
def view_customer():
    data = load_data()
    customer_id = input("Enter Customer ID: ")
    if customer_id not in data:
        print("Customer ID not found.")
        return

    customer = data[customer_id]
    print(f"Customer Name: {customer['name']}")
    print("Loans:")
    for loan in customer["loans"]:
        balance = calculate_balance(customer_id, loan)
        print(f"  Amount: {loan['amount']}, Interest Rate: {loan['interest_rate']}%, Duration: {loan['duration']} months")
        print(f"  Outstanding Balance: {balance}")
        print("  Payments:")
        for payment in loan["payments"]:
            print(f"    Date: {payment['date']}, Amount: {payment['amount']}")

# View all customers
def view_all_customers():
    data = load_data()
    if not data:
        print("No customers in the system.")
        return

    print("All Customers:")
    for customer_id, customer in data.items():
        print(f"ID: {customer_id}, Name: {customer['name']}")

# Delete a customer
def delete_customer():
    data = load_data()
    customer_id = input("Enter Customer ID to delete: ")
    if customer_id not in data:
        print("Customer ID not found.")
        return

    del data[customer_id]
    save_data(data)
    print("Customer deleted successfully.")

# Delete a loan
def delete_loan():
    data = load_data()
    customer_id = input("Enter Customer ID: ")
    if customer_id not in data:
        print("Customer ID not found.")
        return

    loans = data[customer_id]["loans"]
    if not loans:
        print("No active loans found for this customer.")
        return

    print("Active Loans:")
    for i, loan in enumerate(loans):
        print(f"{i + 1}. Amount: {loan['amount']}, Start Date: {loan['start_date']}")

    loan_index = int(input("Select Loan Number to delete: ")) - 1
    if loan_index < 0 or loan_index >= len(loans):
        print("Invalid loan selection.")
        return

    del loans[loan_index]
    save_data(data)
    print("Loan deleted successfully.")

# Search customers by name
def search_customers():
    data = load_data()
    search_name = input("Enter customer name to search: ").lower()

    print("Search Results:")
    found = False
    for customer_id, customer in data.items():
        if search_name in customer["name"].lower():
            print(f"ID: {customer_id}, Name: {customer['name']}")
            found = True
    if not found:
        print("No customers found with that name.")

# Main menu
def main_menu():
    while True:
        print("\nLoan Management System")
        print("1. Add Customer")
        print("2. Add Loan")
        print("3. Make Payment")
        print("4. View Customer Details")
        print("5. View All Customers")
        print("6. Delete Customer")
        print("7. Delete Loan")
        print("8. Search Customers")
        print("9. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            add_customer()
        elif choice == "2":
            add_loan()
        elif choice == "3":
            make_payment()
        elif choice == "4":
            view_customer()
        elif choice == "5":
            view_all_customers()
        elif choice == "6":
            delete_customer()
        elif choice == "7":
            delete_loan()
        elif choice == "8":
            search_customers()
        elif choice == "9":
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
