from odoo import models,fields,api

class Material(models.Model):
    _name = 'product.material'
    _description = 'Product Material'

    name = fields.Char(string='Name')
    currency_id = fields.Many2one(comodel_name='res.currency', string="Currency")
    cost = fields.Monetary(store=True,readonly=False,currency_field='currency_id',string='Cost')
