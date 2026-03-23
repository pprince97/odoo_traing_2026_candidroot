from odoo import models,fields,api

class ResConfigSetting(models.TransientModel):
    _inherit = 'res.config.settings'

    fine_amount_per_dayy = fields.Float(string="Fine Amount Per Day",config_parameter='library_management.fine_amount_per_dayy')

