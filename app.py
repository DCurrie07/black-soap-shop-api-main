from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://bb2ef251680853:f96c55a9@us-cdbr-east-04.cleardb.com/heroku_b1238e369440257'
db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)

    def __init__(self, username, password, first_name, last_name):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name

class Admin(db.Model):
    admin_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)

    def __init__(self, username, password, first_name, last_name):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name

class Product(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Decimal(10,2), nullable=False)

    def __init__(self, name, description, price):
        self.name = name
        self.description = description
        self.price = price

class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "password", "first_name", "last_name")
user_schema = UserSchema()
multiple_user_schema = UserSchema(many=True)

class AdminSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "password", "first_name", "last_name")
admin_schema = AdminSchema()
multiple_admin_schema = AdminSchema(many=True)

class ProductSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "description", "price")
product_schema = ProductSchema()
multiple_product_schema = ProductSchema(many=True)


@app.route("/user/add", methods=["POST"])
def add_user():
    if request.centent_type != "application/json":
        return jsonify("Error, Data must be sent as JSON")
    post_data = request.get_json()
    username = post_data.get("username")
    password = post_data.get("password")
    first_name = post_data.get("first_name")
    last_name = post_data.get("last_name")

    new_record = User(username, password, first_name, last_name)
    db.session.add(new_record)
    db.session.commit()
    return jsonify(user_schema.dump(new_record))

    

    