from odoo import models,fields,api

class ProductMaterial(models.Model):
    _name = 'product.material'
    _description = 'Product Material'

    name = fields.Char(string='Product Name')
    company_currency_id = fields.Many2one('res.currency',string='Company Currency')
    price = fields.Monetary(string='Price',currency_field='company_currency_id')