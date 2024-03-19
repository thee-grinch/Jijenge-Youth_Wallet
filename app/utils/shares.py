from sql.models_alchemy import Share

#a function that creates shares
def new_share(db, user_id, amount):
    share = db.query(Share).filter(Share.user_id == user_id).first()
    if share:
        share.amount += amount
        db.commit()
        return {'message': 'share was updated successfully'}
    share = Share(user_id=user_id, amount=amount)
    db.add(share)
    db.commit()
    return {'message': 'share was added successfully'}
