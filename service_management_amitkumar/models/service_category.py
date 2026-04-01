from odoo import models, fields, api

class ServiceCategory(models.Model):
    _name = 'service.category'
    _description = 'Service Category'

    name = fields.Char(string='Service Category Name')
    # amount = fields.Float(string='Service Category Amount')

    companies_id = fields.Many2one('service.company', string='Company')

    service_ids = fields.One2many('product.template', 'service_category_id', string='Services')