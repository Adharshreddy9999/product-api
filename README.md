# Product Management API

## Overview
The Product Management API is a RESTful service that allows you to manage product inventory with robust validation and error handling.

* Version: 1.0.0
* Base URL: http://localhost:5000
* Support: [GitHub Repository](https://github.com/Adharshreddy9999/product-api)

## Features

* CRUD operations for products
* Input validation
* Error handling
* Logging
* Database persistence
* Swagger UI documentation

## Technical Stack

* Framework: Flask
* Database: PostgreSQL
* ORM: SQLAlchemy
* Validation: Marshmallow
* Documentation: Swagger/OpenAPI 3.0

## Setup and Installation

1. Clone the repository:
```bash
git clone https://github.com/Adharshreddy9999/product-api.git
cd product-api
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set environment variables:
```bash
set DATABASE_URL=postgresql://postgres:979797@localhost:5432/product_db
set FLASK_APP=run.py
set FLASK_ENV=development
```

5. Initialize database:
```bash
flask db upgrade
```

6. Run the application:
```bash
python run.py
```

The application will be available at:
- Web Interface: http://localhost:5000
- API Documentation: http://localhost:5000/api/docs
- API Endpoints: http://localhost:5000/api/products

## API Endpoints

### 1. List All Products
`GET /api/products`

Retrieves a list of all products in the inventory.

Response (200 OK):
```json
[
    {
        "id": 1,
        "name": "Sample Product",
        "description": "A detailed description of the product",
        "price": 29.99,
        "stock": 100,
        "category": "Electronics",
        "created_at": "2025-04-21T01:38:11+05:30",
        "updated_at": "2025-04-21T01:38:11+05:30"
    }
]
```

### 2. Create Product
`POST /api/products`

Creates a new product in the inventory.

Validation Rules:
- Name: Required, maximum 100 characters
- Price: Required, must be non-negative
- Stock: Required, must be non-negative

Request Body:
```json
{
    "name": "New Product",
    "description": "Product description",
    "price": 29.99,
    "stock": 100,
    "category": "Electronics"
}
```

Response (201 Created):
```json
{
    "id": 1,
    "name": "New Product",
    "description": "Product description",
    "price": 29.99,
    "stock": 100,
    "category": "Electronics",
    "created_at": "2025-04-21T01:38:11+05:30",
    "updated_at": "2025-04-21T01:38:11+05:30"
}
```

### 3. Get Product by ID
`GET /api/products/{product_id}`

Retrieves a specific product by its ID.

Response (200 OK):
```json
{
    "id": 1,
    "name": "Sample Product",
    "description": "A detailed description of the product",
    "price": 29.99,
    "stock": 100,
    "category": "Electronics",
    "created_at": "2025-04-21T01:38:11+05:30",
    "updated_at": "2025-04-21T01:38:11+05:30"
}
```

### 4. Update Product
`PUT /api/products/{product_id}`

Updates an existing product.

Validation Rules:
- Name: Maximum 100 characters
- Price: Must be non-negative
- Stock: Must be non-negative

Request Body:
```json
{
    "name": "Updated Product",
    "description": "Updated description",
    "price": 39.99,
    "stock": 150,
    "category": "Electronics"
}
```

Response (200 OK):
```json
{
    "id": 1,
    "name": "Updated Product",
    "description": "Updated description",
    "price": 39.99,
    "stock": 150,
    "category": "Electronics",
    "created_at": "2025-04-21T01:38:11+05:30",
    "updated_at": "2025-04-21T01:38:11+05:30"
}
```

### 5. Delete Product
`DELETE /api/products/{product_id}`

Deletes a product from the inventory.

Response (200 OK):
```json
{
    "message": "Product deleted successfully"
}
```

## Error Responses

### 1. Validation Error (400 Bad Request)
```json
{
    "error": "Validation error",
    "message": "Price cannot be negative"
}
```

### 2. Not Found Error (404 Not Found)
```json
{
    "error": "Product not found"
}
```

### 3. Server Error (500 Internal Server Error)
```json
{
    "error": "Internal server error"
}
```

## Testing the API

1. Using Swagger UI:
   - Visit http://localhost:5000/api/docs
   - Use the interactive documentation to test endpoints

2. Using cURL:
```bash
# List all products
curl http://localhost:5000/api/products

# Create a product
curl -X POST http://localhost:5000/api/products \
  -H "Content-Type: application/json" \
  -d '{"name":"Test Product","price":29.99,"stock":100}'
```

## Error Logging

The application logs errors and events to:
- Console (for development)
- logs/app.log (for production)

## Security Considerations

1. Input Validation
   - All inputs are validated before processing
   - Prevents negative prices and stock values
   - Enforces maximum length for text fields

2. Error Handling
   - Sanitized error messages
   - No sensitive information in responses
   - Proper HTTP status codes

## Future Enhancements

1. Authentication and Authorization
2. Rate Limiting
3. Product Categories Management
4. Image Upload Support
5. Advanced Search and Filtering
6. Pagination Support

## Support

For support and bug reports, please create an issue on our [GitHub repository](https://github.com/Adharshreddy9999/product-api).
