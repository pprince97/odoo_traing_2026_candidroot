from odoo import models, api, fields,Command

class RentalOrder(models.Model):
    _name = 'rental.order'
    _description = 'Rental Order'

    customer_id = fields.Many2one('res.partner',string="Customer",ondelete='cascade')
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    total_amount = fields.Float(string="Total Amount", compute='_compute_total_amount')
    states = fields.Selection([('draft', 'Draft'), ('rent', 'Rent'), ('returned', 'Returned'), ('invoiced', 'Invoiced'),
                               ('partially_invoiced', 'Partially Invoiced'), ('cancelled', 'Cancelled')],
                              string="States", default='draft')

    rental_order_ids = fields.One2many('rental.order.lines', 'rental_order_id', string="Rental Orders")

    def rent_status(self):
        self.update({'states': 'rent'})

    def returned_status(self):
        for order in self.rental_order_ids:
            for piece in order.available_pieces_ids:
                piece.is_available = False
        self.update({'states': 'returned'})

    def cancelled_status(self):
        self.update({'states': 'cancelled'})

    @api.depends('rental_order_ids', 'start_date', 'end_date')
    def _compute_total_amount(self):
        for rec in self:
            rec.total_amount = 0
            if rec.rental_order_ids and rec.start_date and rec.end_date:
                for order in rec.rental_order_ids:
                    rec.total_amount += order.total_amount * (rec.end_date - rec.start_date).days

    def generate_invoice(self):
        res = self.env['account.move'].with_context(
            {'default_move_type': 'in_invoice'}).create({'partner_id': self.customer_id.id, 'invoice_date': fields.Date.today()})
        for order in self.rental_order_ids:
            self.env['account.move.line'].create(
                {'move_id': res.id, 'product_id': order.product_id.id, 'price_unit': order.total_amount})
        self.states = 'partially_invoiced'
        res.update({'state': 'posted'})

        return {
            'name': 'Bill',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_id': res.id,
            'res_model': 'account.move',
            'target': 'self',
        }