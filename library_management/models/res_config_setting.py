from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    fines_amounts_book = fields.Float(config_parameter='library_management.fines_amounts_book', string="Book Fine Amount")