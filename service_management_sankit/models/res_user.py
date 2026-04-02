from odoo import models, fields

class Contact(models.Model):
    _inherit = "res.user"

    city_id = fields.Many2one('res.city',string='City')