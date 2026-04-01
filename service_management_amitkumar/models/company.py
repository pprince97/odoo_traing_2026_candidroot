from odoo import fields, models, api


class Company(models.Model):
    _name = 'service.company'
    _description = 'Company'

    owner_id = fields.Many2one('res.users', string='Owner')
    name = fields.Char(string="Company Name")
    phone = fields.Char(string="Phone Number")
    email = fields.Char(string="Email Address")

    description = fields.Text(string='Description')

    service_category_ids = fields.One2many('service.category', 'companies_id', string='Service Categories')

    service_ids = fields.One2many('product.template', 'companies_id', string='Services')

    service_request_ids = fields.One2many('service.request', 'companies_id', string='Service Requests')
