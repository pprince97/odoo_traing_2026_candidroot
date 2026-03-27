from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    school_id = fields.Many2one('school.object')