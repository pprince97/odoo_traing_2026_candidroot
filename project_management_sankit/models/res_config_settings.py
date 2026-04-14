

from odoo import _, fields, models
from odoo.exceptions import UserError


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    show_create_bill_button = fields.Boolean(string="Show Create Bill Button",config_parameter='project_management_sankit.show_create_bill_button')