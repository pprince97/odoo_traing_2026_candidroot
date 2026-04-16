from odoo import api, fields, models

class Part(models.Model):
    _inherit = 'product.product'

    # name , standard_price is in product.product
    is_what = fields.Selection([
        ('car', 'Car'),
        ('part', 'Part'),
        ('product', 'Product'),
    ])
