from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://fnuuxwzjwsaonp:0a1a91a42db7d1106195fddac81afd7e24f04adc7fccb0ec7d678a36f1eaf8f8@ec2-54-147-207-184.compute-1.amazonaws.com:5432/d8mv8hm3m19p3k'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
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
    __tablename__ = 'admin'
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
    __tablename__ = 'product'
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Integer, nullable=False)

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
    if request.content_type != "application/json":
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

@app.route("/user/get", methods=["GET"])
def get_all_users():
    all_users = User.query.all()
    return jsonify(user_schema.dump(all_users))

@app.route("/user/verfication", methods=["POST"])
def verification():
    if request.content_type != "application/json":
        return jsonify("Error, Data must be sent as JSON")
    post_data = request.get_json()
    username = post_data.get("username")
    password = post_data.get("password")

    user = db.session.query(User).filter(User.username == username).first()

    if user is None:
        return jsonify("User NOT Verified")

    if user.password != password:
        return jsonify("User NOT Verified")
    
    return jsonify("User Verified")

@app.route("/admin/add", methods=["POST"])
def add_admin():
    if request.content_type != "application/json":
        return jsonify("Error, Data must be sent as JSON")
    post_data = request.get_json()
    username = post_data.get("username")
    password = post_data.get("password")
    first_name = post_data.get("first_name")
    last_name = post_data.get("last_name")

    new_record = Admin(username, password, first_name, last_name)
    db.session.add(new_record)
    db.session.commit()
    return jsonify(admin_schema.dump(new_record))

@app.route("/admin/verfication", methods=["POST"])
def admin_verification():
    if request.content_type != "application/json":
        return jsonify("Error, Data must be sent as JSON")
    post_data = request.get_json()
    username = post_data.get("username")
    password = post_data.get("password")

    admin = db.session.query(Admin).filter(Admin.username == username).first()

    if admin is None:
        return jsonify("Admin NOT Verified")

    if admin.password != password:
        return jsonify("Admin NOT Verified")
    
    return jsonify("Admin Verified")


if __name__ == "__main__":
    app.run(debug=True)
    

    