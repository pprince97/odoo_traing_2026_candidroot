from odoo import models,fields,api,_
from odoo.exceptions import ValidationError

class ServiceCompany(models.Model):
    _name = 'custom.service.company'
    _description = 'Company'

    name = fields.Char(string='Company Name')
    phone = fields.Char(string='Phone Number')
    email = fields.Char(string='Email Address')
    address = fields.Char(string='Address')
    owner_id = fields.Many2one('res.users', string='Owner',domain=lambda self: [('group_ids', 'in', self.env.ref('service_management_system_jui.service_group_owner').id)])
    service_category_ids = fields.One2many('service.category','company_id_s',string='Service Categories')
    service_ids = fields.One2many('product.template','company_id_s',string='Services')
    service_request_ids = fields.One2many('service.request','company_id_s',string='Service Requests')