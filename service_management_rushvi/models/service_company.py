from odoo import models,fields,api,_
from odoo.exceptions import ValidationError

class ServiceCompany(models.Model):
    _name = 'service.company'
    _description = 'Service Company'

    name = fields.Char(string='Company Name')
    registration_number = fields.Char(string='Registration Number')
    owner_id = fields.Many2one('res.partner',string='Owner')
    zip = fields.Integer(string='Zip')
    phone = fields.Integer(string='Phone')
    email = fields.Char(string='Email')
    country_id = fields.Many2one('res.country',string='Country')
    state = fields.Many2one('res.country.state',string='State',domain=[('country_id','=',country_id)])
    city = fields.Char(string='City')
    category_ids = fields.One2many('product.template','company_id',string='Services')