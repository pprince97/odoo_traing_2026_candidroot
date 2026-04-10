from odoo import models,fields,api,_

class CustomWidget(models.Model):
    _name = 'custom.widget'
    _description = 'Custom Widget'

    name = fields.Char(string="Name")
    status_text = fields.Char(string="Status Text")