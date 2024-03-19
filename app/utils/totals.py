import datetime
from sqlalchemy.orm import Session
from sql.models_alchemy import Total

def find_total(db: Session, amount: int, col: str):
    today = datetime.datetime.now()
    month = today.strftime("%b")
    year = today.year
    id = "{}-{}".format(month, year)
    total = db.query(Total).filter(Total.id == id).first()
    if not total:
        new_total = Total(id=id, col=amount)
        db.add(new_total)
        db.commit()
    else:
        total.col += amount
        db.commit()

def fetch_totals(db: Session):
    data = {}
    latests = db.query(Total).order_by(Total.date).limit(6).all()
    if not latests:
        return {'message': 'no data found'}
    else:
        for latest in latests:
            name = latest.id.split('-')[0]
            data[name] = latest.savings
    return data
        