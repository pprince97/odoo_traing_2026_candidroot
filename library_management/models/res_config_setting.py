from odoo import fields, models, api

class ResConfigSetting(models.TransientModel):
    _inherit = 'res.config.settings'

    is_active_fine = fields.Boolean(config_parameter='is_active_fine')
    fine_per_day_ = fields.Float(string="Fine per day",config_parameter='fine_per_day_')