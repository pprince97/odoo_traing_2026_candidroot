from odoo import fields,models

class Material(models.Model):
    _name = 'product.material'
    _description = 'Product Material'

    name = fields.Char(string='Material Name')
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, default=lambda self: self.env.user.company_id.currency_id)
    price = fields.Monetary(string='Price',currency_field='currency_id')