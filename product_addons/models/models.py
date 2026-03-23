from odoo import models,fields,api

class ProductInfo(models.Model):
    _name='product.info'
    _description='Product Info'

    name=fields.Char()
    description=fields.Text()
    product_image = fields.Image()
    type=fields.Selection([('electronic','Electronic'),('decor','Decor'),
                           ('kitchen','Kitchen'),('furniture','Furniture')])
    price = fields.Float()
    available=fields.Integer()
    order_date_time=fields.Datetime()
    delivery_date=fields.Date()
    subscriber=fields.Boolean(default=True)
    product_review=fields.Binary()

# license
# application
# manifest version
# model
    # Char
    # Text
    # Selection
    # Integer
    # Float
    # Date
    # Datetime
    # Binary
    # Image
    # Boolean
