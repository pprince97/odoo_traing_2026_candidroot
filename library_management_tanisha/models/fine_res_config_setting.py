from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    fine_amount = fields.Float(string='Fine amount', config_parameter='fine_amount')
