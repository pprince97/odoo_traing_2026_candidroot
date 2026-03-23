from odoo import models,fields,api

class UVPrinting(models.Model):
    _name = 'product.uvprinting'
    _description = 'Product UV Printing'

    name = fields.Char(string='Name')
    currency_id = fields.Many2one(comodel_name='res.currency', string="Currency")
    cost = fields.Monetary(store=True,readonly=False,currency_field='currency_id',string='Cost')
