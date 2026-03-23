from odoo import models,fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    fine_amount = fields.Integer(string="Project Bill",config_parameter='project_management_urvi.fine_amount')
