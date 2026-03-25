from odoo import fields, models,api

class Product(models.Model):
    _inherit = 'product.template'

    product_taxonomy_ids = fields.Many2many('product.taxonomy','product_product_taxonomy_rel','product_id','taxonomy_id',string='Product Taxonomy')