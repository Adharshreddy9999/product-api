from marshmallow import Schema, fields, validate
from decimal import Decimal

class ProductSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    description = fields.Str(validate=validate.Length(max=500))
    price = fields.Decimal(required=True, validate=validate.Range(min=Decimal('0.01')))
    stock = fields.Int(required=True, validate=validate.Range(min=0))
    category = fields.Str(validate=validate.Length(max=50))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
