from odoo import models,fields,api

class ProductConfig(models.Model):
    _inherit = 'product.product'

    rental_order_ids = fields.Many2many(comodel_name='rental.order', relation='product_rent_rel',column1='product_id', column2='rental_order_id', string='Rental Orders')
    # stock_lot_ids = fields.One2many(comodel_name='stock.lot',inverse_name='product_id', string='Stock Lots')


