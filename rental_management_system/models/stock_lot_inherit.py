from odoo import models, fields, api


class ProductProduct(models.Model):
    _inherit = 'stock.lot'

    is_available = fields.Boolean(string="Available", default=True)