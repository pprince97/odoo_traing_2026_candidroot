from odoo import fields,models,api

class Company(models.Model):
    _name = 'service.company'
    _description = 'Company'

    name = fields.Char(string='Company Name')
    owner_id = fields.Many2one('res.users', string='Company Owner')
    active = fields.Boolean(string='Is active? ')
    logo = fields.Binary(string="Logo")
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone Number')
    website = fields.Char(string='Website')
    address = fields.Text(string='Address')
    description = fields.Text(string='About')
    service_category_ids = fields.One2many(comodel_name='service.category',inverse_name='company_id', string='Service Categories')
    service_ids = fields.One2many(comodel_name='product.template',inverse_name='belong_company_id', string='Services')
    request_ids = fields.One2many(comodel_name='service.request', inverse_name='company_id', string='Service Requests')


