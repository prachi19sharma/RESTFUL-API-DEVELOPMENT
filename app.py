from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enables CORS so frontend like HTML/JS can call APIs

# SQLite Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Model for Inventory Item
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=True)
    in_stock = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'quantity': self.quantity,
            'price': self.price,
            'category': self.category,
            'in_stock': self.in_stock
        }

# Create DB if not exists
with app.app_context():
    db.create_all()

# ----------- ROUTES -----------

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Inventory API with SQLite!"})

@app.route('/api/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([item.to_dict() for item in items])

@app.route('/api/items/out-of-stock', methods=['GET'])
def get_out_of_stock_items():
    out_of_stock = Item.query.filter_by(in_stock=False).all()
    return jsonify([item.to_dict() for item in out_of_stock])

@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = Item.query.get(item_id)
    if item:
        return jsonify(item.to_dict())
    return jsonify({'error': 'Item not found'}), 404

@app.route('/api/items', methods=['POST'])
def add_item():
    data = request.get_json()

    if not all(k in data for k in ('name', 'quantity', 'price', 'category')):
        return jsonify({'error': 'Missing item data'}), 400

    item = Item(
        name=data['name'],
        quantity=data['quantity'],
        price=data['price'],
        category=data['category'],
        in_stock=data.get('in_stock', data['quantity'] > 0)
    )
    db.session.add(item)
    db.session.commit()

    return jsonify(item.to_dict()), 201

@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.get_json()
    item = Item.query.get(item_id)

    if not item:
        return jsonify({'error': 'Item not found'}), 404

    item.name = data.get('name', item.name)
    item.quantity = data.get('quantity', item.quantity)
    item.price = data.get('price', item.price)
    item.category = data.get('category', item.category)
    item.in_stock = data.get('in_stock', item.quantity > 0)

    db.session.commit()
    return jsonify(item.to_dict())

@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = Item.query.get(item_id)

    if not item:
        return jsonify({'error': 'Item not found'}), 404

    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item deleted'}), 200

# ----------- SEARCH ROUTE -----------

@app.route('/api/items/search', methods=['GET'])
def search_items():
    query = request.args.get('q', '').strip()

    if not query:
        return jsonify({'error': 'Search term is required'}), 400

    results = Item.query.filter(
        (Item.name.ilike(f"%{query}%")) |
        (Item.category.ilike(f"%{query}%"))
    ).all()

    return jsonify([item.to_dict() for item in results])

# ----------- RUN APP -----------

if __name__ == '__main__':
    app.run(debug=True)
