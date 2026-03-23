from odoo import models, fields, api

class Customcar(models.Model):
    _name = 'custom.car'
    _description = 'Custom Object car'

    model = fields.Char(string="Model")
    make = fields.Integer(string="Make")
    color = fields.Float(string="Color")
    accident = fields.Boolean(string="Accident")
    price = fields.Char(string="Price")
