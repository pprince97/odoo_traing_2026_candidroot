from odoo import api, models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    test_demo = fields.Boolean(string="Demo",config_parameter='project_management.test_demo')