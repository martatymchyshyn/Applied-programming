from flask import Flask, request, jsonify
from marshmallow import Schema
from slugify import slugify
from api_response import Response
from modules import User, Ad, Session, Location
from flask_httpauth import HTTPBasicAuth

app = Flask('__name__')

session = Session()
auth = HTTPBasicAuth()


class UserSchema(Schema):
    class Meta:
        model = User
        fields = ('id', 'user_name', 'first_name', 'last_name', 'location_id')


class AdSchema(Schema):
    class Meta:
        model = Ad
        fields = ('id', 'title', 'body', 'user_id')

@app.route("/api/v1/hello-world-20")
def index():
    return "Hello World 20"

@app.route("/api/v1/users", methods=["POST"])
def create_user():
    user = request.get_json()
    response = create_user_util(user)
    return response.get_json(), response.code

@app.route("/api/v1/users/me", methods=["GET"])
@auth.login_required
def get_user():
    user = auth.current_user()
    response = get_user_by_id(user.id)
    return response.get_json(), response.code

@app.route("/api/v1/users", methods=["GET"])
def get_all_users():
    response = get_all_users_util()
    return response.get_json(), response.code


@app.route("/api/v1/users", methods=["PUT"])
@auth.login_required
def update_user():
    user = auth.current_user()
    update_data = request.get_json()
    response = update_user_util(user.id, update_data)
    return response.get_json(), response.code

@app.route("/api/v1/users", methods=["DELETE"])
@auth.login_required
def delete_user():
    user = auth.current_user()
    response = delete_user_util(user.id)
    return response.get_json(), response.code

@app.route("/api/v1/locations", methods = ["POST"])
@auth.login_required
def create_location():
    user_id = auth.current_user().id
    location_dto = request.get_json()
    response = create_location_util(user_id, location_dto)
    return response.get_json(), response.code

@app.route("/api/v1/ads", methods = ["POST"])
@auth.login_required
def create_add():
    ad_dto = request.get_json()
    user = auth.current_user()
    response = create_ad_util(user, ad_dto)
    return response.get_json(), response.code

@app.route("/api/v1/ads", methods=['GET'])
@auth.login_required
def get_all_ads():
    user = auth.current_user()
    response = get_all_ads_util(user)
    return response.get_json(), response.code

@app.route("/api/v1/ads/<int:ad_id>", methods=['DELETE'])
@auth.login_required
def delete_ad(ad_id):
    user = auth.current_user()
    response = delete_ad_util(ad_id, user.id)
    return response.get_json(), response.code

@app.route('/api/v1/ads/public', methods=['GET'])
def fetch_public_ads():
    public_ads = get_public_ads()
    public_list_dto = AdSchema(many=True)
    return jsonify(public_list_dto.dump(public_ads)), 200

@app.route('/api/v1/ads/my', methods = ['GET'])
@auth.login_required
def fetch_my_ads():
    user = auth.current_user()
    response = get_my_ads_util(user.id)
    return response.get_json(), response.code


def get_my_ads_util(user_id):
    try:
        my_ads = session.query(Ad).filter_by(user_id=int(user_id)).all()
    except:
        my_ads = []

    dto_list = AdSchema(many=True)
    return Response(dto_list.dump(my_ads), 200)

def delete_ad_util(ad_id, user_id):
    try:
        ad = session.query(Ad).filter_by(id=ad_id).one()
    except:
        return Response("Ad not found, cannot delete ad", 404)

    if(ad.user_id != user_id):
        return Response("User is not authorized to delete this ad", 401)

    session.delete(ad)
    session.commit()
    return Response("Ad deleted", 200)

def get_all_ads_util(user):
    public_ads = get_public_ads()

    if user.location == None:
        current_location_ads = []
    else:
        current_location_ads = get_ads_by_location(user.location_id)

    ads_response = public_ads + current_location_ads
    ad_list = AdSchema(many=True)
    return Response(ad_list.dump(ads_response), 200)

def get_ads_by_location(location_id):

    try:
        users = session.query(User).filter_by(location_id=location_id).all()
        ads = []
        for user in users:
            ads += session.query(Ad).filter_by(user_id=user.id).all()
    except:
        return []

    return ads

def get_public_ads():
    try:
        ads = session.query(Ad).filter_by(is_public=True).all()
    except:
        ads = []

    return ads

def create_ad_util(user, ad_dto):

    if user.location == None:
        return Response('User cannot create ad without location', 400)

    ad = Ad(**ad_dto)
    ad.user_id = user.id

    if not ad_dto.get('is_public', None):
         ad.is_public = False
    else:
        ad.is_public = True

    session.add(ad)
    session.commit()

    return Response("Ad created", 201)

def create_location_util(user_id, location_dto):

    user = session.query(User).filter_by(id=int(user_id)).one()

    location_name = slugify(location_dto['name'])
    location_dto['name'] = location_name

    if not check_if_location_exist(location_name):
        if not create_location(location_dto):
            return Response("Something went wrong", 400)

    location = session.query(Location).filter_by(name=location_name).one()

    user.location_id = location.id

    session.commit()
    return Response('Location created', 201)

def get_all_users_util():
    user_list = UserSchema(many=True)
    try:
        users = session.query(User).all()
    except:
        users = []


    return Response(user_list.dump(users), 200)

def delete_user_util(user_id):

    user = session.query(User).filter_by(id=user_id).one()

    try:
        ads = session.query(Ad).filter_by(user_id = user.id).all()
    except:
        ads = []

    session.delete(user)
    for ad in ads:
        session.delete(ad)

    session.commit()

    return Response("User deleted", 200)

def update_user_util(user_id, update_data):

    user = session.query(User).filter_by(id=user_id).one()

    try:
        if update_data.get('first_name', None):
            user.first_name = update_data['first_name']
        if update_data.get('last_name', None):
            user.last_name = update_data['last_name']
        if update_data.get('user_name', None):
            if check_if_user_exists_by_username_util(update_data['user_name']):
                return Response('Such user name already exists', 400)
            user.user_name = update_data['user_name']
        if update_data.get('password', None):
            user.password = update_data['password']
    except:
        return Response("Invalid Input", 400)
    session.commit()
    session.close()

    return Response('Updated', 200)

def get_user_by_id(user_id):

    user = session.query(User).filter_by(id=user_id).one()

    return Response(UserSchema().dump(user), 200)



def create_user_util(user):
    try:
        if user["password"] == None :
            return Response('Invalid input, not all fields present', 400)

        user = User(**user)
    except:
        return Response('Invalid input, not all fields present', 400)
    
    if check_if_user_exists_by_username_util(user.user_name):
        return Response("User with this username already exist, username should be unique", 400)
    

    session.add(user)
    session.commit()

    return Response("Created", 201)



def check_if_user_exists_by_username_util(user_name):
    try:
        user = session.query(User).filter_by(user_name=user_name).one()
    except:
        return False

    return True

def check_if_location_exist(location_name):
    try:
        location = session.query(Location).filter_by(name=location_name).one()
    except:
        return False

    return True

def create_location(location_dto):
    try:
        new_location = Location(**location_dto)
        session.add(new_location)
        session.commit()
    except:
        return False

    return True

@auth.verify_password
def authenticate(user_name, password):
    try:
        user = session.query(User).filter_by(user_name=user_name).one()
    except:
        return None

    if not user.password == password:
        return None

    return user

if __name__ == '__main__':
    app.run()