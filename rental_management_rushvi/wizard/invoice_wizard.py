from odoo import models,fields,api
from odoo.exceptions import ValidationError

class Invoice(models.TransientModel):
    _name = 'wizard.invoice.rental.orders'
    _description = 'Invoice Rental Orders'

    amount_to_invoice = fields.Float(string='Amount to Invoice', compute='_compute_amount_to_invoice')
    total_rent_amount = fields.Float(string='Total Amount')
    invoice_amount = fields.Float(string='Invoice Amount')
    rental_order_id = fields.Many2one('rental.order', string='Rental Order')

    @api.depends('invoice_amount', 'total_rent_amount')
    def _compute_amount_to_invoice(self):
        for order in self:
            if order.amount_to_invoice - order.invoice_amount>=0:
                order.amount_to_invoice = order.amount_to_invoice - order.invoice_amount
            else:
                order.amount_to_invoice = order.invoice_amount
                raise ValidationError('Invoice amount cannot be negative')

    def generate_bill(self):
        move = self.env['account.move'].with_context({'default_rental_order_id':self.id,
                                                      'default_task_ids':self.task_ids.ids}).create({
            'move_type': 'in_invoice',
            'partner_id': self.rental_order_id.customer_id.id,
            'invoice_date': fields.Date.today(),
            'invoice_amount': self.invoice_amount,
        })
        move.write({
            'state': 'posted',
        })
        rental = self.env['rental.order'].search(
            [('rental_number', '=', self.env.context.get('rental_number'))], limit=1)
        rental.write({'amount_to_invoice': self.amount_to_invoice,
                      'canceled_date': fields.Datetime.now(),
                      })
        if self.amount_to_invoice > 0:
            rental.write({'state': 'partially_invoiced'})
        else:
            rental.write({'state': 'invoiced'})
