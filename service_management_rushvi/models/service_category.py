from odoo import models,fields,api,_
from odoo.exceptions import ValidationError

class ServiceCategory(models.Model):
    _name = 'service.category'
    _description = 'Service category'

    name = fields.Char(string='Category Name')
    company_id = fields.Many2one('service.company',string='Company')