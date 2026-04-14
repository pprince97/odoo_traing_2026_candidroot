from odoo import models, fields, api
# from datetime import date
# from odoo.exceptions import ValidationError

class RentalObjectLines(models.Model):
    _name = 'rental.object.lines'
    _description = 'Rental Object Line'
    _rec_name = 'product_id'
    _order = 'sequence'

    sequence = fields.Integer(string='Sequence')
    rental_object_id = fields.Many2one('rental.object', string='Rental Object')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    lot_ids = fields.Many2many('stock.lot', 'rental_line_lot_rel', string='Lots', domain="[('product_id', '=', product_id), ('is_available', '=', True)]")
    amount_per_day = fields.Float(string='Amount Per Day', compute='_compute_amount_per_day')
    total_amount = fields.Float(string='Total Amount', compute='_compute_total_amount')


    def _compute_amount_per_day(self):
        for lot in self:
            lot.amount_per_day = lot.product_id.lst_price

    @api.depends('lot_ids', 'product_id')
    def _compute_total_amount(self):
        for lot in self:
            lot.total_amount = lot.amount_per_day