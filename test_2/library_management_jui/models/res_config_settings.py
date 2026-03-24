from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    fine_amount =fields.Integer(string="Fine Amount",config_parameter='library_management_jui.fine_amount')
