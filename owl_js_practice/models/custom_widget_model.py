from odoo import models,api,fields

class CustomWidgetModel(models.Model):
    _name='custom.widget.model'
    _description='custom widget model'

    number = fields.Float(string="Number")