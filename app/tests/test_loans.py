import unittest
from datetime import datetime, timedelta
from sql.models import Loan, LoanType
from utils.loans import *
from dateutil.relativedelta import relativedelta

class TestCalculateAmount(unittest.TestCase):

    def setUp(self):
        self.loan_type = LoanType(type_name="TestType", interest_rate=6, repayment_period=12)
        self.loan_borrowed_date = datetime(2024, 1, 1)
        self.loan = Loan(
            loan_type_id=self.loan_type.loan_type_id,
            user_id=1,
            amount=10000,
            status="pending",
            application_date=self.loan_borrowed_date,
            last_payment_date=None,
            payment_schedule=1,
            balance=10000
        )
    # ... (Previous test cases)

    def test_calculate_amount_with_min_monthly_interest(self):
        self.loan.last_payment_date = self.loan_borrowed_date
        self.loan.total_amount = 10000
        self.assertEqual(calculate_amount(self.loan, self.loan_type), 10050)

    def test_calculate_amount_with_max_monthly_interest(self):
        self.loan.last_payment_date = self.loan_borrowed_date
        self.loan.total_amount = 10000
        self.loan_type.interest_rate = 99
        self.assertEqual(calculate_amount(self.loan, self.loan_type), 10825)

    def test_calculate_amount_with_min_loan_amount(self):
        self.loan.amount = 0
        self.assertEqual(calculate_amount(self.loan, self.loan_type), 0)

    def test_calculate_amount_with_max_loan_amount(self):
        self.loan.amount = 1_000_000_000
        self.assertEqual(calculate_amount(self.loan, self.loan_type), 1_005_000_000)

    def test_calculate_amount_with_no_last_payment_date_and_max_months_since_borrowed(self):
        self.loan.amount = 10000
        self.loan.last_payment_date = None
        self.loan.application_date = datetime(2022, 2, 9)
        self.assertEqual(self.loan.application_date, datetime.now())
        # self.assertEqual(calculate_amount(self.loan, self.loan_type), 22500)

    def test_calculate_amount_with_last_payment_date_in_future(self):
        self.loan.last_payment_date = datetime(2025, 1, 1)
        print(self.loan.application_date)
        self.assertEqual(calculate_amount(self.loan, self.loan_type), 10000)

if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)