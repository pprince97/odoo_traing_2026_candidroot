from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    show_bill =fields.Boolean(string="Show Bill",config_parameter='project_management_jui.show_bill')
