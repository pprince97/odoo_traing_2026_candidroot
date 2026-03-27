from odoo import models, fields, api

class LibrarySettings(models.TransientModel):
    _inherit = 'res.config.settings'



    is_Active_fine = fields.Boolean(string="Fine Amount Per Day",
                                config_parameter='library_management_sunil.is_Active_fine')
    fine_per_days = fields.Float(string="Fine Amount Per Day", default=5, config_parameter='library_management_sunil.fine_per_days')

