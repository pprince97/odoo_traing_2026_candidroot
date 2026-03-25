from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    suitable_for_ids = fields.Many2many(
        'product.tag','suitable_product_rel','product_id','suitable_id',
        string='Suitable For')
