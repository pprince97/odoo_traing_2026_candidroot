from odoo import _, fields, models
from odoo.exceptions import UserError

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'


    project_bill = fields.Boolean(string="Project Bill",config_parameter='project_management_urvi.project_bill')
    project_id = fields.Many2one(comodel_name='project.project.urvi',string="Project",config_parameter='project_management_urvi.project_id')