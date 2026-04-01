from odoo import models, fields

class OwlData(models.Model):
    _name = 'owl.data.storage'
    _description = 'OWL Component Data'

    name = fields.Char(string='Name')
    price = fields.Float(string='Float')
    image = fields.Char(string='Image')
