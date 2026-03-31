from odoo import models,fields,api,_

class Services(models.Model):
    _inherit = 'product.template'

    category_id = fields.Many2one('service.category',string='Service Category')
    company_id_s = fields.Many2one('custom.service.company',string='Company')