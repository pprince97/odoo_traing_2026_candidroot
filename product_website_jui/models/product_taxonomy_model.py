from odoo import fields, models,api

class ProductTaxonomy(models.Model):
    _name = 'product.taxonomy'
    _description = 'Product Taxonomy'

    name = fields.Char(string='Name')
    visible_to_customers = fields.Boolean(default=True)