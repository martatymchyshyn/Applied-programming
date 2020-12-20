from flask import Flask, request
from modules import User, Ad,Session
from api_response import Response
from marshmallow import Schema, fields

app = Flask('__name__')

session = Session()


class UserSchema(Schema):
    class Meta:
        model = User
        fields = ('id', 'user_name', 'first_name', 'last_name', 'location_id')


@app.route("/api/v1/hello-world-20")
def index():
    return "Hello World 20"

@app.route("/api/v1/users", methods=["POST"])
def create_user():
    user = request.get_json()
    response = create_user_util(user)
    return response.get_json(), response.code

@app.route("/api/v1/users/<string:user_name>", methods=["GET"])
def get_user_by_user_name(user_name):
    response = get_user_by_user_name_util(user_name)
    return response.get_json(), response.code

@app.route("/api/v1/users", methods=["GET"])
def get_all_users():
    response = get_all_users_util()
    return response.get_json(), response.code


@app.route("/api/v1/users/<string:user_name>", methods=["PUT"])
def update_user(user_name):
    update_data = request.get_json()
    response = update_user_util(user_name, update_data)
    return response.get_json(), response.code

@app.route("/api/v1/users/<string:user_name>", methods=["DELETE"])
def delete_user(user_name):
    response = delete_user_util(user_name)
    return response.get_json(), response.code


def get_all_users_util():
    user_list = UserSchema(many=True)
    try:
        users = session.query(User).all()
    except:
        users = []

    if len(users) == 0:
        return Response("No users", 200)
    return Response(user_list.dump(users), 200)

def delete_user_util(username):
    if not check_if_user_exists_util(username):
        return Response("User not found, cannot delete user", 404)

    try:
        user = session.query(User).filter_by(user_name=username).one()
    except:
        return Response("Not found", 404)

    try:
        ads = session.query(Ad).filter_by(user_id = user.id).all()
    except:
        ads = []

    session.delete(user)
    for ad in ads:
        session.delete(ad)

    session.commit()

    return Response("User deleted", 200)

def update_user_util(username, update_data):
    if not check_if_user_exists_util(username):
        return Response('User with such user_name does not exist', 404)
    try:
        user = session.query(User).filter_by(user_name=username).one()
    except:
        return Response('Not found', 404)
    try:
        if update_data.get('first_name', None):
            user.first_name = update_data['first_name']
        if update_data.get('last_name', None):
            user.last_name = update_data['last_name']
        if update_data.get('user_name', None):
            if check_if_user_exists_util(update_data['user_name']):
                return Response('Such user name already exists', 400)
            user.user_name = update_data['user_name']
        if update_data.get('password', None):
            user.password = update_data['password']
    except:
        return Response("Invalid Input", 400)
    session.commit()

    return Response('Updated', 200)

def get_user_by_user_name_util(username):

    if not check_if_user_exists_util(username):
        return Response('User with such user_name does not exist', 404)
    
    try:
        user = session.query(User).filter_by(user_name=username).one()
    except:
        return Response('Not found', 404)

    return Response(UserSchema().dump(user), 200)



def create_user_util(user):
    try:
        user = User(**user)
    except:
        return Response('Invalid input, not all fields present', 400)
    
    if check_if_user_exists_util(user.user_name):
        return Response("User with this username already exist, username should be unique", 400)
    

    session.add(user)
    session.commit()

    return Response("Created", 201)



def check_if_user_exists_util(username):
    try:
        user = session.query(User).filter_by(user_name=username).one()
    except:
        return False
    
    return True

if __name__ == '__main__':
    app.run()