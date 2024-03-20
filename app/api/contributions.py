from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from utils.contributions import new_contribution
from sql.database_alchemy import get_db

from utils.totals import find_total
from utils.notifications import new_notification
from utils.oauth import get_current_user
from utils.notifications import new_notification
from utils.transactions import new_transaction

from schemas.contributions import ContributionSchema

router = APIRouter()

@router.post('app/new_contribution')
def new_contribution_route(data: ContributionSchema, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    amount = data.amount
    new_transaction(db, user_id, 'contribution', amount)
    new_notification(db, user_id, 'contribution', amount)
    find_total(db, amount, 'contribution')
    return new_contribution(db,user_id, amount)
