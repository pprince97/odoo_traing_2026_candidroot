from odoo import fields,models

class SurfaceFinish(models.Model):
    _name = 'product.surface.finish'
    _description = 'Product Surface Finish'

    name = fields.Char(string='Surface Finish')
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, default=lambda self: self.env.user.company_id.currency_id)
    price = fields.Monetary(string='Price',currency_field='currency_id')