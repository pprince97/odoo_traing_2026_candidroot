from odoo import models, api, fields,Command

class RentalOrder(models.Model):
    _name = 'rental.order.lines'
    _description = 'Rental Order'

    product_id = fields.Many2one('product.product',string='Products')
    available_pieces_ids = fields.Many2many('stock.lot', 'stock_rental_order_lines_relation','orders_id','product_id',string='Available Pieces')
    total_amount = fields.Float(string='Total Amount')

    rental_order_id = fields.Many2one('rental.order',string='Rental Order')

    @api.onchange('available_pieces_ids')
    def _onchange_available_pieces_ids(self):
        for rec in self:
            if rec.available_pieces_ids:
                for piece in rec.available_pieces_ids:
                    piece.is_available = True
            else:
                for piece in rec.available_pieces_ids:
                    if piece.is_available == True and rec.rental_order_id.states in ['draft','returned','invoiced','partially_invoiced','cancelled']:
                        piece.is_available = False

    @api.onchange('product_id','available_pieces_ids')
    def _onchange_product_id(self):
        for rec in self:
            rec.total_amount = 0
            if rec.product_id:
                res = self.env['stock.lot'].search_count([('id', 'in', rec.available_pieces_ids.ids)])
                rec.total_amount = rec.product_id.lst_price * res
