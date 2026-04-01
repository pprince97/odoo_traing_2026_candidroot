from odoo import api, fields, models

class Category(models.Model):
    _name = 'service.category'
    _description = 'Service Category Model'

    name = fields.Char(string='Category Name',required=True)
    description = fields.Text(string='Description')
    color = fields.Integer(string='Color')
    company_id = fields.Many2one('service.company',string='Company',required=True)