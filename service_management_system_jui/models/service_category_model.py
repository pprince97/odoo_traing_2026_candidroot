from odoo import models,fields,api,_
from odoo.exceptions import ValidationError

class ServiceCategory(models.Model):
    _name = 'service.category'
    _description = 'Service Category'

    name = fields.Char(string='Name')
    service_ids = fields.One2many('product.template','category_id',string='Services')
    company_id_s = fields.Many2one('custom.service.company',string='Company')