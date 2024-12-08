import unittest
import json
import os
from loan import load_data, save_data, add_customer, add_loan, make_payment, calculate_balance

DATA_FILE = "loan_data.json"

class TestLoanManagementSystem(unittest.TestCase):

    def setUp(self):
        """Set up a fresh data file for testing."""
        self.test_data = {
            "C001": {
                "name": "John Doe",
                "loans": [
                    {
                        "amount": 1000.0,
                        "interest_rate": 5.0,
                        "duration": 12,
                        "start_date": "2024-01-01",
                        "payments": []
                    }
                ]
            }
        }
        save_data(self.test_data)

    def tearDown(self):
        """Clean up after tests."""
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)

    def test_load_data(self):
        """Test loading data from the JSON file."""
        data = load_data()
        self.assertEqual(data, self.test_data)

    def test_save_data(self):
        """Test saving data to the JSON file."""
        new_data = {"C002": {"name": "Jane Smith", "loans": []}}
        save_data(new_data)
        with open(DATA_FILE, "r") as file:
            file_data = json.load(file)
        self.assertEqual(file_data, new_data)

    def test_add_customer(self):
        """Test adding a new customer."""
        new_customer_id = "C003"
        data = load_data()
        data[new_customer_id] = {"name": "Alice", "loans": []}
        save_data(data)

        updated_data = load_data()
        self.assertIn(new_customer_id, updated_data)
        self.assertEqual(updated_data[new_customer_id]["name"], "Alice")

    def test_add_loan(self):
        """Test adding a loan to an existing customer."""
        customer_id = "C001"
        loan = {
            "amount": 5000.0,
            "interest_rate": 7.0,
            "duration": 24,
            "start_date": "2024-02-01",
            "payments": []
        }
        data = load_data()
        data[customer_id]["loans"].append(loan)
        save_data(data)

        updated_data = load_data()
        self.assertIn(loan, updated_data[customer_id]["loans"])

    def test_make_payment(self):
        """Test making a payment for an existing loan."""
        customer_id = "C001"
        payment = {"date": "2024-02-15", "amount": 200.0}
        data = load_data()
        data[customer_id]["loans"][0]["payments"].append(payment)
        save_data(data)

        updated_data = load_data()
        self.assertIn(payment, updated_data[customer_id]["loans"][0]["payments"])

    def test_calculate_balance(self):
        """Test calculating the outstanding balance of a loan."""
        customer_id = "C001"
        loan = self.test_data[customer_id]["loans"][0]
        balance = calculate_balance(customer_id, loan)
        expected_balance = loan["amount"] + (loan["amount"] * loan["interest_rate"] / 100)
        self.assertAlmostEqual(balance, expected_balance, places=2)


if __name__ == "__main__":
    unittest.main()
