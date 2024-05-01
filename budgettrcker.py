
import os
import datetime

class Transaction:
    def __init__(self, amount, category, description, date=None):
        self.amount = amount
        self.category = category
        self.description = description
        self.date = date if date else datetime.date.today()

    def __str__(self):
        return f"{self.date}: {self.description} | {self.category}: ${self.amount}"


class BudgetTracker:
    def __init__(self):
        self.transactions = []

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def calculate_balance(self):
        total_income = sum(transaction.amount for transaction in self.transactions if transaction.amount > 0)
        total_expenses = sum(transaction.amount for transaction in self.transactions if transaction.amount < 0)
        return total_income + total_expenses

    def analyze_expenses(self):
        categories = {}
        for transaction in self.transactions:
            if transaction.amount < 0:
                category = transaction.category
                amount = transaction.amount
                categories[category] = categories.get(category, 0) + amount
        return categories

    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            for transaction in self.transactions:
                file.write(f"{transaction.date},{transaction.amount},{transaction.category},{transaction.description}\n")

    def load_from_file(self, filename):
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                for line in file:
                    date_str, amount_str, category, description = line.strip().split(',')
                    date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
                    amount = float(amount_str)
                    self.transactions.append(Transaction(amount, category, description, date))

    def display_transactions(self):
        if not self.transactions:
            print("No transactions found.")
        else:
            for transaction in self.transactions:
                print(transaction)


def get_date_input(prompt):
    while True:
        date_str = input(prompt)
        try:
            date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            return date
        except ValueError:
            print("Invalid date format. Please enter date in YYYY-MM-DD format.")


def main():
    budget_tracker = BudgetTracker()
    filename = "transactions.txt"
    budget_tracker.load_from_file(filename)

    while True:
        print("\n===== Personal Budget Tracker =====")
        print("1. Enter Income")
        print("2. Enter Expense")
        print("3. View Transactions")
        print("4. View Budget Balance")
        print("5. Analyze Expenses")
        print("6. Save and Quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            amount = input("Enter income amount: ")
            if not amount.isdigit():
                print("Invalid amount. Please enter a valid number.")
                continue
            amount = float(amount)
            category = input("Enter income category: ")
            description = input("Enter income description: ")
            date = get_date_input("Enter date (YYYY-MM-DD), leave empty for today: ")
            budget_tracker.add_transaction(Transaction(amount, category, description, date))

        elif choice == "2":
            amount = input("Enter expense amount: ")
            if not amount.isdigit():
                print("Invalid amount. Please enter a valid number.")
                continue
            amount = float(amount)
            category = input("Enter expense category: ")
            description = input("Enter expense description: ")
            date = get_date_input("Enter date (YYYY-MM-DD), leave empty for today: ")
            budget_tracker.add_transaction(Transaction(-amount, category, description, date))

        elif choice == "3":
            budget_tracker.display_transactions()

        elif choice == "4":
            balance = budget_tracker.calculate_balance()
            print(f"Current Budget Balance: ${balance:.2f}")

        elif choice == "5":
            expense_analysis = budget_tracker.analyze_expenses()
            if not expense_analysis:
                print("No expenses recorded for analysis.")
            else:
                print("Expense Analysis:")
                for category, amount in expense_analysis.items():
                    print(f"{category}: ${amount:.2f}")

        elif choice == "6":
            budget_tracker.save_to_file(filename)
            print("Transactions saved. Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
