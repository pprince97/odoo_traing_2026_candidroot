from odoo import models,fields

class ApplicationArea(models.Model):
    _name = 'product.application.area'
    _description = 'Product Application Area'

    name = fields.Char(string='Product Application Area')
    description = fields.Char(string='Description')