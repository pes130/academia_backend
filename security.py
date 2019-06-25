from werkzeug.security import safe_str_cmp
from models.user import UserModel



def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user

# Esta se llama una vez que estás autenticado. Le pasas el jwt token y comprueba si está ok
def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)