from odoo import models, fields

class PriceObject(models.Model):
    _name = "price.object"
    _description = "Product Price"

    name = fields.Char(string='Product Name')
    price_subtotal = fields.Float(string='Subtotal')