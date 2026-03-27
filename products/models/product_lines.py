from odoo import models,fields,api

class ProductLine(models.Model):
    _name = 'product.lines'
    _description = 'Product Lines'

    product_id = fields.Many2one('product.product',string="Product")
    part_product_id = fields.Many2one('product.product',string="Product Parts")
    product_price = fields.Float('Product Price')
    product_quantity = fields.Integer('Product Quantity')
    total_price = fields.Float('Total Price')