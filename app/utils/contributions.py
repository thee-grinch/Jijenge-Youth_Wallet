from sql.models_alchemy import Transaction, Contribution
from utils.totals import find_total

#a function to input monthly contributions, and update transactions
def new_contribution(db, user_id, amount):
    # transaction = Transaction(user_id=user_id, type='contribution', amount=amount)
    contribution = contribution(user_id=user_id, amount=amount)
    # find_total(db, amount, 'contribution')
    db.add(contribution)
    db.commit()
    return {'message': 'contribution was added successfully'}

#a function to get the user's contribution history
def get_contributions(db, user_id):
    contributions = db.query(Contribution).filter(Contribution.user_id == user_id).all()
    if not contributions:
        return {'message': 'no contributions found'}
    data = []
    for contribution in contributions:
        data.append({'amount': contribution.amount, 'date': contribution.date})
    return data