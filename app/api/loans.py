"""
this module describes all the loans endpoints

"""
from fastapi import Depends, APIRouter

from utils.oauth import get_current_user

router = APIRouter()