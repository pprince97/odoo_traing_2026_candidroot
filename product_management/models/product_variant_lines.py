from odoo import models,fields,api

class ProductVariantLines(models.Model):
    _name = 'product.variant.lines'
    _description = 'Product Variant Lines'

    product_id = fields.Many2one(comodel_name='product.product',string='Product')
    sub_product_id = fields.Many2one(comodel_name='product.product', string='Product')
    currency_id = fields.Many2one(comodel_name='res.currency', string="Currency")
    cost = fields.Monetary(store=True, currency_field='currency_id', string='Cost')
    quantity = fields.Integer(string='Quantity')
    total = fields.Monetary(store=True, currency_field='currency_id', string='Total', compute='_compute_total')

    @api.depends('product_id','quantity')
    def _compute_total(self):
        for rec in self:
            rec.cost = rec.sub_product_id.total_cost
            rec.total = rec.quantity * rec.cost

