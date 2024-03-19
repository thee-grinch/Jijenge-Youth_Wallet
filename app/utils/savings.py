from sql.models_alchemy import Saving
# from utils.totals import find_total

#a sunction to create savings
def new_saving(db, user_id, amount):
    saving = db.query(Saving).filter(Saving.user_id == user_id).first()
    if saving:
        saving.amount += amount
        # saving.balance += amount
        db.commit()
        return {'message': 'saving was updated successfully'}
    saving = Saving(user_id=user_id, amount=amount)
    # transaction = Transaction(user_id=user_id, type='saving', amount=amount)
    # find_total(db, amount, 'saving')
    db.add(saving)
    db.commit()
    return {'message': 'saving was added successfully'}