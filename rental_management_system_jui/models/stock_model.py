from odoo import models, api,fields

class Stock(models.Model):
    _inherit = 'stock.lot'

    is_available = fields.Boolean(string="Is available")