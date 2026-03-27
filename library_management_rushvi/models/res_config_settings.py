from odoo import models,fields,api

class LibraryBooks(models.TransientModel):
    _inherit = 'res.config.settings'

    fine_amount = fields.Integer('Fine Amount',default=0,config_parameter='library_management_rushvi.fine_amount')