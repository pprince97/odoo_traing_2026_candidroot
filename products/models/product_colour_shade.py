from odoo import models,fields,api

class ProductColourShade(models.Model):
    _name = 'product.colour.shade'
    _description = 'Product Colour Shade'
    _rec_name = 'shade'

    shade = fields.Integer(string='Shade')
    company_currency_id = fields.Many2one('res.currency',string='Company Currency')
    price = fields.Monetary(string='Price',currency_field='company_currency_id')