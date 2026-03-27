from odoo import models,fields,api

class ProductUVPrinting(models.Model):
    _name = 'product.uv.printing'
    _description = 'Product UV Printing'

    min_range = fields.Integer(string='Minimum Area')
    max_range = fields.Integer(string='Maximum Area')
    company_currency_id = fields.Many2one('res.currency',string='Company Currency')
    price = fields.Monetary(string='Price',currency_field='company_currency_id')