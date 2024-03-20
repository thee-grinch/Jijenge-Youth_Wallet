from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from utils.shares import new_share
from sql.database_alchemy import get_db
from utils.oauth import get_current_user
from utils.notifications import new_notification
from utils.transactions import new_transaction
from utils.totals import find_total

from schemas.shares import ShareSchema

router = APIRouter()

@router.post('/app/new_share')
def new_share_route(data: ShareSchema, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    amount = data.amount
    new_transaction(db, user_id, 'share', amount)
    new_notification(db, user_id, 'share', amount)
    find_total(db, amount, 'share')
    return new_share(db, user_id, amount)