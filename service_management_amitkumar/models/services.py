from odoo import models, fields, api

class Product(models.Model):
    _inherit = 'product.template'

    service_category_id = fields.Many2one('service.category', string='Service Category')
    companies_id = fields.Many2one('service.company', string='Company')
