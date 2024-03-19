from sql.models_alchemy import Transaction


def new_transaction(db, user_id, transaction_type, amount):
    money_in = False if transaction_type == 'loan' else True
    transaction = Transaction(user_id=user_id, TransactionType=transaction_type, Amount=amount, money_in=money_in)
    db.add(transaction)
    db.commit()

# a function to get the user's transaction history
def get_transactions(db, user_id):
    transactions = db.query(Transaction).filter(Transaction.user_id == user_id).all()
    if not transactions:
        return {'message': 'no transactions found'}
    data = []
    for transaction in transactions:
        data.append({'type': transaction.type, 'amount': transaction.amount, 'date': transaction.date, 'money_in': transaction.money_in})
    return data