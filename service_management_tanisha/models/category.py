from odoo import fields,models,api

class ServiceCategory(models.Model):
    _name = 'service.category'
    _description = 'Service Category'

    name = fields.Char(string='Category Name')
    company_id = fields.Many2one(comodel_name='service.company', string='Company')
    service_ids = fields.One2many(comodel_name='product.template',inverse_name='category_id', string='Services')
