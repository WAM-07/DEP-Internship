from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'

db = SQLAlchemy(app)
jwt = JWTManager(app)


# Database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(120), nullable=True)


# Initialize the database
@app.before_first_request
def create_tables():
    db.create_all()


# User registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "User already exists"}), 400

    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


# User login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username, password=password).first()

    if not user:
        return jsonify({"message": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token), 200


# Create a new item
@app.route('/item', methods=['POST'])
@jwt_required()
def create_item():
    data = request.get_json()
    new_item = Item(name=data['name'], description=data.get('description', ''))
    db.session.add(new_item)
    db.session.commit()
    return jsonify({"message": "Item created"}), 201


# Read all items
@app.route('/items', methods=['GET'])
@jwt_required()
def get_items():
    items = Item.query.all()
    return jsonify([{"id": item.id, "name": item.name, "description": item.description} for item in items])


# Update an item
@app.route('/item/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_item(item_id):
    data = request.get_json()
    item = Item.query.get(item_id)

    if not item:
        return jsonify({"message": "Item not found"}), 404

    item.name = data['name']
    item.description = data.get('description', item.description)
    db.session.commit()

    return jsonify({"message": "Item updated"}), 200


# Delete an item
@app.route('/item/<int:item_id>', methods=['DELETE'])
@jwt_required()
def delete_item(item_id):
    item = Item.query.get(item_id)

    if not item:
        return jsonify({"message": "Item not found"}), 404

    db.session.delete(item)
    db.session.commit()

    return jsonify({"message": "Item deleted"}), 200


if __name__ == '__main__':
    app.run(debug=True)
