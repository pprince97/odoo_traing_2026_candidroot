from odoo import fields,models

class ColorShade(models.Model):
    _name = 'product.color.shade'
    _description = 'Product Color Shade'

    name = fields.Char(string='Color Shade Name')
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, default=lambda self: self.env.user.company_id.currency_id)
    price = fields.Monetary(string='Price',currency_field='currency_id')
    color = fields.Integer(string='Color Shade')