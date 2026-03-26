from odoo import models, fields

class SuitableFor(models.Model):
    _name = 'suitable.for'
    _description = 'Suitable For'
    _rec_name = 'name'

    name = fields.Char(string='Name')

