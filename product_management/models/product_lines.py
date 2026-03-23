from odoo import fields,models,api

class ProductLines(models.Model):
    _name = "product.product.lines"
    _description = "Product Lines"

    product_id = fields.Many2one('product.product',string='Products',ondelete='cascade')
    sub_product_id = fields.Many2one('product.product',string='Products',ondelete='cascade')
    quantity = fields.Integer(string='Quantity',default=1)
    cost = fields.Float(string='Product Cost')
    total = fields.Float(string='Total Cost',compute='_compute_total')

    @api.depends('quantity','cost')
    def _compute_total(self):
        for product in self:
            product.total = product.cost * product.quantity

    @api.onchange('sub_product_id')
    def _onchange_product_id(self):
        for product in self:
            if product.sub_product_id:
                product.cost = product.sub_product_id.total_cost
            else:
                product.cost = 0

