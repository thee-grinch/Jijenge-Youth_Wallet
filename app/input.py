from faker import Faker
from sql.models_alchemy import *
from sqlalchemy.orm import Session
from utils.utils import hash_pass

fake = Faker()
def add_user(db: Session):
    user_data = {
        'name': fake.user_name(),
        'password': hash_pass('1234'),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "is_verified": fake.boolean(),
        "registration_date": fake.date_time_this_year(),
        "last_login_date": fake.date_time_this_year()
    }
    user = User(**user_data)
    db.add(user)
    db.commit()
    db.refresh(user)
    # Generate dummy data for contributions, loans, savings, notifications, guarantors, shares, and transactions
    contribution = Contribution(user_id=user.id, amount=fake.random_int(min=1000, max=5000))
    loan_type = LoanType(type_name="Personal Loan", interest_rate=5.0, repayment_period=12)
    loan = Loan(user_id=user.id, amount=5000, loan_type=loan_type)
    saving = Saving(user_id=user.id, amount=fake.random_int(min=1000, max=5000), balance=fake.random_int(min=1000, max=5000))
    notification = Notification(user_id=user.id, title="New Notification", message="You have a new notification")
    guarantor = Guarantors(user_id=user.id, loan_id=loan.loan_id, date=datetime.now())
    share = Shares(user_id=user.id, amount=fake.random_int(min=100, max=500))
    transaction = Transactions(user_id=user.id, TransactionType="Deposit", Amount=fake.random_int(min=100, max=500))
    administrator = Administrator(user_id=user.id, title="Admin")

    db.add_all([contribution, loan_type, loan, saving, notification, guarantor, share, transaction, administrator])
    db.commit() 