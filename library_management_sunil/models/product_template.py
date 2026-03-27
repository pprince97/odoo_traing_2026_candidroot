from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    is_top_selling = fields.Boolean(string='Top Selling', help='Mark this product as top-selling for homepage display.')
