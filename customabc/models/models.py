from odoo import models, fields, api

class CustomAbc(models.Model):
    _name = 'custom.abc'
    _description = 'Custom Object Abc'

    name = fields.Char(string="Name")
    age = fields.Integer(string="Age")
    percentage = fields.Float(string="Percentage")
    description = fields.Text(string="Description")
# customabc.access_custom_form,access_custom_form,customabc.model_custom_form,,1,1,1,1