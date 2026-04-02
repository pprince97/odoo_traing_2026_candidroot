from odoo import api, fields, models

from odoo.exceptions import ValidationError

class Company(models.Model):
    _name = 'company.object'
    _description = 'Company'
    _rec_name = 'name'

    name = fields.Char(string='Company Name')
    owner_id = fields.Many2one('res.users', string='Company Owner')

