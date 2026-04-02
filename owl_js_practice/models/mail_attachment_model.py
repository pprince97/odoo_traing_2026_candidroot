from odoo import models,api,fields

class CustomMailModel(models.TransientModel):
    _inherit='mail.compose.message'

    attach_files = fields.Binary(string="Attach files")