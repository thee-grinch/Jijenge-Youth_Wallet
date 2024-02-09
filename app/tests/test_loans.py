import unittest
from datetime import datetime, timedelta
from utils.loans import approve_loan, calculate_amount, calculate_balance, calculate_payment_schedule, Loan, LoanType

class TestLoanFunctions(unittest.TestCase):
    def test_approve_loan(self):
        loan1 = Loan(status="pending")
        approve_loan(loan1)
        self.assertEqual(loan1.status, "approved")

        loan2 = Loan(status="rejected")
        approve_loan(loan2)
        self.assertEqual(loan2.status, "approved")

        # Test with already approved loan
        loan3 = Loan(status="approved")
        approve_loan(loan3)
        self.assertEqual(loan3.status, "approved")

    def test_calculate_amount(self):
        # Test with current amount less than or equal to borrowed amount
        loan1 = Loan(amount=1000, total_amount=1000)
        loan_type1 = LoanType(interest_rate=5)
        self.assertEqual(calculate_amount(loan1, loan_type1), 1000)

        # Test with current amount greater than borrowed amount and last payment date not set
        loan2 = Loan(amount=1000, total_amount=1100)
        loan_type2 = LoanType(interest_rate=5)
        self.assertEqual(calculate_amount(loan2, loan_type2), 1100)

        # Test with current amount greater than borrowed amount and last payment date set
        loan3 = Loan(amount=1000, total_amount=1100, last_payment_date=datetime.now() - timedelta(days=40))
        loan_type3 = LoanType(interest_rate=5)
        self.assertEqual(calculate_amount(loan3, loan_type3), 1150)

        # Test with zero borrowed amount
        loan4 = Loan(amount=0, total_amount=100)
        loan_type4 = LoanType(interest_rate=5)
        self.assertEqual(calculate_amount(loan4, loan_type4), 100)

        # Test with zero interest rate
        loan5 = Loan(amount=1000, total_amount=1050)
        loan_type5 = LoanType(interest_rate=0)
        self.assertEqual(calculate_amount(loan5, loan_type5), 1050)

        # Test with negative borrowed amount
        loan6 = Loan(amount=-1000, total_amount=1000)
        loan_type6 = LoanType(interest_rate=5)
        self.assertEqual(calculate_amount(loan6, loan_type6), 1000)

        # Test with negative interest rate
        loan7 = Loan(amount=1000, total_amount=1050)
        loan_type7 = LoanType(interest_rate=-5)
        self.assertEqual(calculate_amount(loan7, loan_type7), 1050)

        # Test with zero total amount
        loan8 = Loan(amount=1000, total_amount=0)
        loan_type8 = LoanType(interest_rate=5)
        self.assertEqual(calculate_amount(loan8, loan_type8), 0)

        # Test with negative total amount
        loan9 = Loan(amount=1000, total_amount=-100)
        loan_type9 = LoanType(interest_rate=5)
        self.assertEqual(calculate_amount(loan9, loan_type9), -95)

        # Test with zero interest rate and zero total amount
        loan10 = Loan(amount=1000, total_amount=0)
        loan_type10 = LoanType(interest_rate=0)
        self.assertEqual(calculate_amount(loan10, loan_type10), 0)

    def test_calculate_balance(self):
        loan1 = Loan(total_paid=500, total_amount=1000)
        calculate_balance(loan1)
        self.assertEqual(loan1.balance, -500)

        # Test with zero total paid
        loan2 = Loan(total_paid=0, total_amount=1000)
        calculate_balance(loan2)
        self.assertEqual(loan2.balance, -1000)

        # Test with zero total amount
        loan3 = Loan(total_paid=500, total_amount=0)
        calculate_balance(loan3)
        self.assertEqual(loan3.balance, 500)

        # Test with negative total paid
        loan4 = Loan(total_paid=-500, total_amount=1000)
        calculate_balance(loan4)
        self.assertEqual(loan4.balance, 1500)

        # Test with negative total amount
        loan5 = Loan(total_paid=500, total_amount=-1000)
        calculate_balance(loan5)
        self.assertEqual(loan5.balance, -1500)

        # Test with zero total paid and zero total amount
        loan6 = Loan(total_paid=0, total_amount=0)
        calculate_balance(loan6)
        self.assertEqual(loan6.balance, 0)

        # Test with negative total paid and negative total amount
        loan7 = Loan(total_paid=-500, total_amount=-1000)
        calculate_balance(loan7)
        self.assertEqual(loan7.balance, 500)

        # Test with zero total paid and negative total amount
        loan8 = Loan(total_paid=0, total_amount=-1000)
        calculate_balance(loan8)
        self.assertEqual(loan8.balance, 1000)

        # Test with negative total paid and zero total amount
        loan9 = Loan(total_paid=-500, total_amount=0)
        calculate_balance(loan9)
        self.assertEqual(loan9.balance, -500)

        # Test with zero balance
        loan10 = Loan(total_paid=1000, total_amount=1000)
        calculate_balance(loan10)
        self.assertEqual(loan10.balance, 0)

    def test_calculate_payment_schedule(self):
        loan1 = Loan(amount=1000, total_amount=1100, application_date=datetime.now() - timedelta(days=60))
        loan_type1 = LoanType(interest_rate=5, repayment_period=12)
        calculate_payment_schedule(loan1, loan_type1)
        self.assertAlmostEqual(loan1.payment_schedule, 8.333, places=3)

        loan2 = Loan(amount=1000, total_amount=1100, application_date=datetime.now() - timedelta(days=20))
        loan_type2 = LoanType(interest_rate=5, repayment_period=12)
        calculate_payment_schedule(loan2, loan_type2)
        self.assertAlmostEqual(loan2.payment_schedule, 1100/10, places=3)

        # Test with zero amount and zero total amount
        loan3 = Loan(amount=0, total_amount=0, application_date=datetime.now() - timedelta(days=20))
        loan_type3 = LoanType(interest_rate=5, repayment_period=12)
        calculate_payment_schedule(loan3, loan_type3)
        self.assertAlmostEqual(loan3.payment_schedule, 0)

        # Test with negative amount and negative total amount
        loan4 = Loan(amount=-1000, total_amount=-1100, application_date=datetime.now() - timedelta(days=20))
        loan_type4 = LoanType(interest_rate=5, repayment_period=12)
        calculate_payment_schedule(loan4, loan_type4)
        self.assertAlmostEqual(loan4.payment_schedule, -1100/10, places=3)

        # Test with zero repayment period
        loan5 = Loan(amount=1000, total_amount=1100, application_date=datetime.now() - timedelta(days=20))
        loan_type5 = LoanType(interest_rate=5, repayment_period=0)
        calculate_payment_schedule(loan5, loan_type5)
        self.assertAlmostEqual(loan5.payment_schedule, 0)

        # Test with negative repayment period
        loan6 = Loan(amount=1000, total_amount=1100, application_date=datetime.now() - timedelta(days=20))
        loan_type6 = LoanType(interest_rate=5, repayment_period=-12)
        calculate_payment_schedule(loan6, loan_type6)
        self.assertAlmostEqual(loan6.payment_schedule, 0)

        # Test with zero interest rate
        loan7 = Loan(amount=1000, total_amount=1100, application_date=datetime.now() - timedelta(days=20))
        loan_type7 = LoanType(interest_rate=0, repayment_period=12)
        calculate_payment_schedule(loan7, loan_type7)
        self.assertAlmostEqual(loan7.payment_schedule, 1100/12, places=3)

        # Test with negative interest rate
        loan8 = Loan(amount=1000, total_amount=1100, application_date=datetime.now() - timedelta(days=20))
        loan_type8 = LoanType(interest_rate=-5, repayment_period=12)
        calculate_payment_schedule(loan8, loan_type8)
        self.assertAlmostEqual(loan8.payment_schedule, 1100/12, places=3)

        # Test with zero total amount
        loan9 = Loan(amount=1000, total_amount=0, application_date=datetime.now() - timedelta(days=20))
        loan_type9 = LoanType(interest_rate=5, repayment_period=12)
        calculate_payment_schedule(loan9, loan_type9)
        self.assertAlmostEqual(loan9.payment_schedule, 0)

        # Test with negative total amount
        loan10 = Loan(amount=1000, total_amount=-1100, application_date=datetime.now() - timedelta(days=20))
        loan_type10 = LoanType(interest_rate=5, repayment_period=12)
        calculate_payment_schedule(loan10, loan_type10)
        self.assertAlmostEqual(loan10.payment_schedule, 1100/12, places=3)

if __name__ == "__main__":
    unittest.main()
