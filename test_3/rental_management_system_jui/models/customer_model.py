from odoo import models, api,fields

class Customer(models.Model):
    _inherit = 'res.partner'

    is_customer = fields.Boolean(string="Customer")