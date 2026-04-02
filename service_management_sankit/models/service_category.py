from odoo import api, fields, models

class ServiceCategory(models.Model):
    _name = 'service.category'
    _description = 'Service Category'
    _rec_name = 'service_name'

    service_name = fields.Char(string="Service Category")
    company_id = fields.Many2one('company.object', string="Company")
    owner_id = fields.Many2one(related='company_id.owner_id', string="Owner")