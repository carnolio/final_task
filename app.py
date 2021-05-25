from flask import Flask, jsonify, request, redirect
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
import pymysql
from config import Config
from hashids import Hashids
from flask_cors import CORS
import hashlib

app = Flask(__name__)
app.config.from_object(Config)

client = app.test_client()

engine = create_engine(f'mysql+pymysql://{Config.db_user}:{Config.db_pass}@{Config.db_host}/{Config.db_name}')

session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = session.query_property()


from models import *


jwt = JWTManager(app)

cors = CORS(app, resources={
    r"/*": {"origins": Config.CORS_ALLOWED_ORIGINS}
})

hashids = Hashids(min_length=12, salt=Config.salt)




# Создаем таблицы в БД
# Раскоментируй строчку ниже, если нужно первоначальное создание таблиц
#Base.metadata.create_all(bind=engine)

def gen_link_hash(origin_link):
    shorted_link = hashlib.sha256(origin_link.encode("UTF-8")).hexdigest()
    return shorted_link[:14]

@app.route('/register', methods=['POST'])
def register():
    #print('sdasd')
    params = request.json
    user = User(**params)
    session.add(user)
    session.commit()
    token = user.get_token()
    print('qqq', user.name)
    return {'access_token': token}


@app.route('/login', methods=['POST'])
def login():
    params = request.json
    user = User.authenticate(**params)
    token = user.get_token()
    user_id = user.id
    return {'access_token': token, 'user_id': user_id}


@app.route('/add-link', methods=['POST'])
@jwt_required()
def add_link():
    user_id = get_jwt_identity()
    new_one = Link(**request.json)
    new_one.user_id = user_id
    new_one.counter = 0
    session.add(new_one)
    session.commit()
    if new_one.friendly_link:
        friendly = new_one.friendly_link
    else:
        friendly = ""
    serialized = {
        'original': new_one.original,
        'type_id': new_one.type_id,
        'friendly': friendly,
        'counter': new_one.counter,
        "user_id": user_id
    }
    return jsonify(serialized)


@app.route('/links', methods=['GET'])
@jwt_required()
def get_list():
    user_id = get_jwt_identity()
    links = Link.query.filter(Link.user_id == user_id)
    serialized = []
    for link in links:
        if link.friendly_link:
            friendly_link = f"{Config.api_url}/{link.friendly_link}"
        else:
            friendly_link = ''
        serialized.append({
            'id': link.id,
            'original': link.original,
            'friendly': friendly_link,
            'short': f"{Config.api_url}/{hashids.encode(link.id)}",
            'counter': link.counter,
        })
    return jsonify(serialized)


@app.route('/links/<int:link_id>', methods=['PUT'])
@jwt_required()
def update_link(link_id):
    user_id = get_jwt_identity()
    item = Link.query.filter(Link.id == link_id, Link.user_id == user_id).first()
    params = request.json
    if not item:
        return {'message': 'Нет ссылок с таким id'}, 400
    for key, value in params.items():
        setattr(item, key, value)
    session.commit()
    serialized = {
        'type_id': item.type_id,
        'friendly': item.friendly_link
    }
    return serialized


@app.route('/links/<int:link_id>', methods=['DELETE'])
@jwt_required()
def delete_link(link_id):
    user_id = get_jwt_identity()
    item = Link.query.filter(Link.id == link_id, Link.user_id == user_id).first()
    if not item:
        return {'message': 'Нет ссылок с таким id'}, 400
    session.delete(item)
    session.commit()
    return '', 204


@app.route('/<short_uri>')
def url_redirect(short_uri):
    link_id = hashids.decode(short_uri)
    if link_id:
        type_query = "id"
        link = Link.get_original_link(*link_id, type_query)
    else:
        type_query = "fl"
        link = Link.get_original_link(short_uri, type_query)
    if link:
        print(link)
        original_link = link.original
        if link.type_id == 1:
            link.counter += 1
            session.commit()
            return redirect(original_link)
        elif link.type_id == 2:
            if check_autentificate():
                link.counter += 1
                session.commit()
                return redirect(original_link)
        else:
            if check_private_link(link.user_id):
                link.counter += 1
                session.commit()
                return redirect(original_link)
            else:
                return {'message': 'Недостаточно прав'}, 400
    return {'message': 'Ссылка недействительна'}, 400


@jwt_required()
def check_autentificate():
    return get_jwt_identity()


@jwt_required()
def check_private_link(link_user_id):
    user_id = get_jwt_identity()
    if user_id == link_user_id:
        return True


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


if __name__ == '__main__':
    app.run(host=Config.api_host, port=Config.api_port)
