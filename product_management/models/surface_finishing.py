from odoo import models,fields,api

class SurfaceFinishing(models.Model):
    _name = 'product.surface.finishing'
    _description = 'Product Surface Finishing'

    name = fields.Char(string='Surface Name')
    currency_id = fields.Many2one(comodel_name='res.currency', string="Currency")
    cost = fields.Monetary(store=True,readonly=False,currency_field='currency_id',string='Cost')
