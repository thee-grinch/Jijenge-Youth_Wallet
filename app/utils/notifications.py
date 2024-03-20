from sql.models_alchemy import Notification

#a function that creates new notification
def new_notification(db, user_id, transaction_type, amount, guarantor=None, loan_id=None):
    if transaction_type == "loan":
        title = "Loan borrowed"
        message = f"You have borrowed a loan of {amount}"
    elif transaction_type == "payment":
        title = "Loan payment"
        message = f"You have paid a loan of {amount}"
    elif transaction_type == "saving":
        title = "Saving added"
        message = f"You have added {amount} to your savings"
    elif transaction_type == "share":
        title = "Share added"
        message = f"You have added {amount} to your shares"
    elif transaction_type == "contribution":
        title = "Contribution added"
        message = f"You have added {amount} to your contributions"
    elif guarantor:
        title = "Loan guarantor"
        message = f"you have been added as a guarantor to a loan {loan_id}"
    else:
        pass
    notification = Notification(user_id=user_id, title=title, message=message)
    db.add(notification)
    db.commit()

# a function that gets the user's notifications
def get_notifications(db, user_id):
    notifications = db.query(Notification).filter(Notification.user_id == user_id).all()
    if not notifications:
        return {'message': 'no notifications found'}
    data = []
    for notification in notifications:
        data.append({'title': notification.title, 'message': notification.message})
    return data