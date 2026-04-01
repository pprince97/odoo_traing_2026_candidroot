from odoo import fields, models

class ProductTemplates(models.Model):
    _inherit = "product.template"

    service_category_id = fields.Many2one('service.category',string='Service Category',required=True)
    service_company_id = fields.Many2one('service.company',string='Service Company',required=True)
