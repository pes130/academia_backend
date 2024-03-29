from flask_restful import Resource, reqparse
from models.user import UserModel
from models.blacklist import BlacklistModel
from flask_jwt_extended import create_access_token, create_refresh_token, get_raw_jwt, jwt_refresh_token_required, jwt_required, get_jwt_identity, fresh_jwt_required
import hashlib


_user_parser = reqparse.RequestParser()
_user_parser.add_argument(
    "username",
    type=str,
    required=True,
    help="This field cannot be blank"
)
_user_parser.add_argument(
    "password",
    type=str,
    required=True,
    help="This field cannot be blank"
)

class User(Resource):
    

    def get(self, user_id):
        user = UserModel.find_by_id(user_id)
        if user:
            return user.json()
        return {
                   "message": "User not found!"
               }, 404

    @fresh_jwt_required
    def delete(self, user_id):
        user = UserModel.find_user_by_id(user_id)
        if user:
            user.remove_from_db()
            return {
                       "message": "User deleted!"
                   }, 200

        return {
                   "message": "User not found!"
               }, 404

class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data["username"]):
            return {
                    "message": "User exists!"
                }, 400

        user = UserModel(data["username"], hashlib.sha256(data["password"].encode("utf-8")).hexdigest())
        user.save_to_db()
        return {"message": "User {} created!".format(data["username"])}


class UserLogin(Resource):
    def post(self):
        data = _user_parser.parse_args()

        print(data)
        user = UserModel.find_by_username(data["username"])

        if user and user.password == hashlib.sha256(data["password"].encode("utf-8")).hexdigest():
            access_token = create_access_token(identity=user.id, fresh=True)  # Puts User ID as Identity in JWT
            refresh_token = create_refresh_token(identity=user.id)  # Puts User ID as Identity in JWT

            return {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "code": 200
                }, 200

        return {
                "message": "Invalid credentials!",
                "code": 401
            }, 401

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user_id = get_jwt_identity()  # Gets Identity from JWT
        new_token = create_access_token(identity=current_user_id, fresh=False)
        return {
                "access_token": new_token,
                "code": 200
            }, 200

class TokenExpire(Resource):
    @jwt_required
    def delete(self):
        jti = get_raw_jwt()['jti']
        token2Add = BlacklistModel(jti)
        token2Add.save_to_db()
        return {
                "message": "Successfully logged out",
                "code": 200
            }, 200


    @classmethod
    def is_token_expired(cls, token):
        return BlacklistModel.find_by_token(token)

    