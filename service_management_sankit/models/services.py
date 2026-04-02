from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _description = 'Product Template'

    service_category_id = fields.Many2one('service.category', string='Service Category')
    service_company_id = fields.Many2one('company.object', string='Company')
    owner_id = fields.Many2one(related='service_category_id.owner_id', string='Owner')
