from odoo import api, fields, models

class CustomWidget(models.Model):
    _name = 'customwidget.widget'
    _description = 'Custom Widget'

    name = fields.Char('Name')