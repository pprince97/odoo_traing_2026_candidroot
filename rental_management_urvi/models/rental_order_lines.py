from odoo import models,fields,api

class RentalOrderLines(models.Model):
    _name='rental.order.lines'
    _description='Rental Order'

    order_id=fields.Many2one('rental.order',string='Rental Order')
    product_id =fields.Many2one('product.product',string='Product',required=True)
    serial_ids = fields.Many2many('stock.lot','rental_stock_rel','rental_id','stock_id',string='Product Numbers',required=True)
    rent = fields.Float(string='Cost',compute='_compute_rent',store=True)
    quantity = fields.Integer(string='Quantity',compute='_compute_quantity',store=True)
    total_rent = fields.Float(string='Total',compute='_compute_total_rent',store=True)
    used_serial_ids = fields.Many2many('stock.lot','used_stock_rel','used_id','stock_id',string='Used Products',required=True,compute='_compute_used_serial_ids')


    @api.depends('product_id')
    def _compute_rent(self):
        for rec in self:
                rec.rent = rec.product_id.lst_price

    @api.depends('serial_ids')
    def _compute_quantity(self):
        for rec in self:
            rec.quantity = len(rec.serial_ids.ids)

    @api.depends('quantity','rent','order_id.days')
    def _compute_total_rent(self):
        for rec in self:
            if rec.order_id.days:
                rec.total_rent = rec.quantity * rec.rent * rec.order_id.days

    @api.depends('product_id')
    def _compute_used_serial_ids(self):
        for rec in self:
            if rec:
                rec.used_serial_ids = self.env['rental.order.lines'].search(
                    [('order_id.state', 'in', ['rent']), ('product_id', '=', self.product_id)]).serial_ids