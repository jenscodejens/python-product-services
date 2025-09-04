from flask import Flask, jsonify, request
from db import db
from Product import Product

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@db/products'
""" app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:password@db:3306/products' """

db.init_app(app)

# For debug
@app.route("/ping", methods=["POST"])
def ping():
    return {"msg": "pong"}, 200

@app.route('/products', methods=['GET'])
def get_products():
    products = [product.json for product in Product.find_all()]
    return jsonify(products)

@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.find_by_id(id)
    if product:
        return jsonify(product.json)
    return f"Product with id:{id} not found", 404

@app.route('/products', methods=['POST'])
def post_product():
    print('POST /product')

    # Retrieve the product from the request body
    request_product = request.json

    # Create the new product
    product = Product(None, request_product['name'])

    # Save the product to db
    product.save_to_db()

    # Return the jsonified product
    return jsonify(product.json), 201

@app.route('/products/<int:id>', methods=['PUT'])
def put_product(id):
    existing_product = Product.find_by_id(id)

    if existing_product:
        # Get the request payload
        updated_product = request.json

        existing_product.name = updated_product['name']
        existing_product.save_to_db()

        return jsonify(existing_product.json), 200

    return f'Product with {id} not found', 404


@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    existing_product = Product.find_by_id(id)
    if existing_product:
        existing_product.delete_from_db()
        return jsonify({
            'message': f'Deleted product with id {id}'
        }), 200
    
    return f'Product with id:{id} not found', 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')




