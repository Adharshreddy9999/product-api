from flask import Blueprint, jsonify, request, render_template, redirect, url_for, current_app
from .models import db, Product
from .schemas import product_schema, products_schema
from sqlalchemy.exc import SQLAlchemyError

# Create blueprints
main = Blueprint('main', __name__)
api = Blueprint('api', __name__, url_prefix='/api')

# API Error Handlers
@api.errorhandler(404)
def handle_404(e):
    return jsonify({"error": "Resource not found"}), 404

@api.errorhandler(SQLAlchemyError)
def handle_sqlalchemy_error(e):
    return jsonify({"error": "Database error occurred"}), 500

@api.errorhandler(Exception)
def handle_generic_error(e):
    return jsonify({"error": "Internal server error"}), 500

# API Routes
@api.route('/')
def api_root():
    return jsonify({
        "message": "Welcome to the Product Management API",
        "version": "1.0.0",
        "endpoints": {
            "List all products": "/api/products",
            "Get product by ID": "/api/products/<id>",
            "Create product": "/api/products",
            "Update product": "/api/products/<id>",
            "Delete product": "/api/products/<id>",
            "API Documentation": "/api/docs"
        }
    })

@api.route('/products', methods=['GET'])
def get_products():
    try:
        products = Product.query.all()
        current_app.logger.info('Successfully retrieved all products')
        return jsonify(products_schema.dump(products))
    except Exception as e:
        current_app.logger.error(f'Error retrieving products: {str(e)}')
        raise

@api.route('/products', methods=['POST'])
def create_product():
    try:
        data = request.get_json()
        if not data:
            current_app.logger.warning('No data provided in request')
            return jsonify({"error": "No data provided"}), 400

        new_product = Product(
            name=data['name'],
            description=data.get('description', ''),
            price=data['price'],
            stock=data['stock'],
            category=data.get('category', '')
        )
        
        db.session.add(new_product)
        db.session.commit()
        
        current_app.logger.info(f'Successfully created product: {new_product.name}')
        return jsonify(product_schema.dump(new_product)), 201
    
    except ValueError as e:
        current_app.logger.warning(f'Validation error while creating product: {str(e)}')
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    except KeyError as e:
        current_app.logger.warning(f'Missing required field: {str(e)}')
        return jsonify({"error": f"Missing required field: {str(e)}"}), 400
    except SQLAlchemyError as e:
        current_app.logger.error(f'Database error while creating product: {str(e)}')
        db.session.rollback()
        return jsonify({"error": "Database error occurred"}), 500
    except Exception as e:
        current_app.logger.error(f'Unexpected error while creating product: {str(e)}')
        db.session.rollback()
        raise

@api.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    try:
        product = Product.query.get_or_404(id)
        current_app.logger.info(f'Successfully retrieved product: {product.name}')
        return jsonify(product_schema.dump(product))
    except Exception as e:
        current_app.logger.error(f'Error retrieving product {id}: {str(e)}')
        raise

@api.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    try:
        product = Product.query.get_or_404(id)
        data = request.get_json()
        if not data:
            current_app.logger.warning('No data provided in request')
            return jsonify({"error": "No data provided"}), 400
        
        if 'name' in data:
            product.name = data['name']
        if 'description' in data:
            product.description = data['description']
        if 'price' in data:
            product.price = data['price']
        if 'stock' in data:
            product.stock = data['stock']
        if 'category' in data:
            product.category = data['category']
        
        db.session.commit()
        current_app.logger.info(f'Successfully updated product: {product.name}')
        return jsonify(product_schema.dump(product))
    
    except ValueError as e:
        current_app.logger.warning(f'Validation error while updating product: {str(e)}')
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    except SQLAlchemyError as e:
        current_app.logger.error(f'Database error while updating product: {str(e)}')
        db.session.rollback()
        return jsonify({"error": "Database error occurred"}), 500
    except Exception as e:
        current_app.logger.error(f'Unexpected error while updating product: {str(e)}')
        db.session.rollback()
        raise

@api.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    try:
        product = Product.query.get_or_404(id)
        product_name = product.name
        
        db.session.delete(product)
        db.session.commit()
        
        current_app.logger.info(f'Successfully deleted product: {product_name}')
        return jsonify({"message": "Product deleted successfully"}), 200
    
    except SQLAlchemyError as e:
        current_app.logger.error(f'Database error while deleting product: {str(e)}')
        db.session.rollback()
        return jsonify({"error": "Database error occurred"}), 500
    except Exception as e:
        current_app.logger.error(f'Unexpected error while deleting product: {str(e)}')
        db.session.rollback()
        raise

# Web Routes
@main.route('/')
def index():
    try:
        products = Product.query.all()
        current_app.logger.info('Successfully loaded index page')
        return render_template('index.html', products=products)
    except Exception as e:
        current_app.logger.error(f'Error loading index page: {str(e)}')
        raise

@main.route('/add_product')
def add_product():
    try:
        current_app.logger.info('Loading add product form')
        return render_template('product_form.html', product=None)
    except Exception as e:
        current_app.logger.error(f'Error loading add product form: {str(e)}')
        raise

@main.route('/edit_product/<int:id>')
def edit_product(id):
    try:
        product = Product.query.get_or_404(id)
        current_app.logger.info(f'Loading edit form for product: {product.name}')
        return render_template('product_form.html', product=product)
    except Exception as e:
        current_app.logger.error(f'Error loading edit product form: {str(e)}')
        raise
