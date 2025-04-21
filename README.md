# Product Management API

A RESTful API built with Flask and PostgreSQL for managing product inventory.

## Features

- CRUD operations for products
- PostgreSQL database with SQLAlchemy ORM
- Input validation with Marshmallow
- Error handling and logging
- API documentation with Swagger UI
- Docker support with docker-compose
- CORS support
- Web interface for product management

## Prerequisites

- Docker and Docker Compose
- Python 3.9+ (for local development)
- PostgreSQL (for local development)

## Quick Start with Docker

1. Clone the repository:
```bash
git clone <repository-url>
cd product-api
```

2. Start the application with Docker Compose:
```bash
docker-compose up --build
```

The application will be available at:
- API Documentation: http://localhost:5000/api/docs
- API Endpoints: http://localhost:5000/api/

## Local Development Setup

1. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables in `.env`:
```env
DATABASE_URL=postgresql://postgres:979797@localhost:5432/product_db
SECRET_KEY=your-secret-key
FLASK_APP=run.py
FLASK_ENV=development
```

4. Initialize the database:
```bash
flask db upgrade
```

5. Run the development server:
```bash
flask run
```

## API Documentation

### Base URL
`http://localhost:5000/api`

### Authentication
Currently, the API does not require authentication.

### Endpoints

#### GET /products
Get all products.

Response:
```json
[
  {
    "id": 1,
    "name": "Product Name",
    "description": "Product Description",
    "price": 99.99,
    "stock": 10,
    "category": "Category",
    "created_at": "2025-04-20T12:00:00Z",
    "updated_at": "2025-04-20T12:00:00Z"
  }
]
```

#### POST /products
Create a new product.

Request Body:
```json
{
  "name": "Product Name",
  "description": "Product Description",
  "price": 99.99,
  "stock": 10,
  "category": "Category"
}
```

#### GET /products/{id}
Get a specific product by ID.

#### PUT /products/{id}
Update a specific product.

Request Body:
```json
{
  "name": "Updated Name",
  "price": 149.99,
  "stock": 15
}
```

#### DELETE /products/{id}
Delete a specific product.

### Error Responses

The API uses conventional HTTP response codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 404: Not Found
- 500: Internal Server Error

Error Response Format:
```json
{
  "error": "Error message",
  "details": {
    "field": ["Error details"]
  }
}
```

## Logging

Logs are stored in `app.log` with rotation enabled:
- Maximum log file size: 10KB
- Backup count: 3 files
- Log format: `timestamp level: message`

## Database Schema

### Products Table
- id: Integer (Primary Key)
- name: String(100)
- description: String(500)
- price: Decimal(10,2)
- stock: Integer
- category: String(50)
- created_at: DateTime
- updated_at: DateTime

## Project Structure

```
product_api/
├── app/
│   ├── __init__.py      # Flask application factory
│   ├── models.py        # Database models
│   ├── routes.py        # API routes
│   ├── schemas.py       # Marshmallow schemas
│   └── config.py        # Configuration
├── migrations/          # Database migrations
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker Compose configuration
├── requirements.txt    # Python dependencies
├── run.py             # Application entry point
└── README.md          # Project documentation
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.
