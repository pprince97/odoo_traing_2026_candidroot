from odoo import models,fields,api

class Product(models.Model):
    _inherit = 'product.product'

    # used_serial_ids = fields.Many2many('stock.lot','used_stock_rel','used_id','stock_id',string='Used Products',required=True,compute='_compute_used_serial_ids')
    line_ids = fields.One2many('rental.order.lines','product_id',string='Lines')

    @api.model
    def default_get(self, fields):
        defaults = super(Product, self).default_get(fields)
        if defaults:
            defaults['is_storable'] = True
            defaults['tracking'] = 'serial'
        return defaults

    # @api.depends('line_ids.product_id')
    # def _compute_used_serial_ids(self):
    #     for rec in self:
    #         if rec:
    #             rec.used_serial_ids = self.env['rental.order.line'].search(
    #                 [('state', 'in', ['rent']), ('product_id', '=', self.id)]).serial_ids

