from odoo import models,fields,api

class StockLot(models.Model):
    _inherit = 'stock.lot'

    # product_id = fields.Many2one(comodel_name='product.product', string='Product')