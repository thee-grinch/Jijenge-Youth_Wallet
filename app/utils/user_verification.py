from itsdangerous import URLSafeTimedSerializer, exc
from fastapi import HTTPException


SECRET_KEY = "7578d28c002681e9f33ba3949f7c2ff18ca96d5ec1f34cd7bfb5b8aa43f9591b"
serializer = URLSafeTimedSerializer(SECRET_KEY)

def create_link(email: str):
    '''creates an email link for verification'''
    token = serializer.dumps(email)
    url = 'http://jijenge.muvandii.tech/app/verify'
    verification_link = '{}/?token={}'.format(url, token)
    return verification_link
def decode_token(token: str):
    '''receturns an email from the token'''
    try:
        return(serializer.loads(token, max_age=1600))
    except exc.SignatureExpired:
        raise HTTPException(status_code=400, detail='verification link has expired')
    except exc.BadSignature:
        raise HTTPException(status_code=400, detail='Invalid verification code')
