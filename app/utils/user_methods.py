from sql.models_alchemy import User

def user_dict(user:User):
    data = {}
    attrs = ['name', 'first_name', 'last_name', 'email', 'last_login_date']
    for key, value in user.__dict__.items():
        if key in attrs:
            data[key] = value
    
    return data