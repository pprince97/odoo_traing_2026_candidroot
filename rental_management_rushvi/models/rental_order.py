from odoo import models,fields,api
from odoo.exceptions import ValidationError

from dateutil.relativedelta import relativedelta


class RentalOrder(models.Model):
    _name = "rental.order"
    _description = "Rental Order"
    _rec_name = "rental_number"

    rental_number = fields.Char(string="Rental Number")
    customer_id = fields.Many2one("res.partner",string="Customer")
    rent_start_date = fields.Datetime(string="Start Date")
    rent_end_date = fields.Datetime(string="End Date")
    rental_order_line_ids = fields.One2many('rental.order.lines','rental_order_id',string="Rental Order Lines")
    currency_id = fields.Many2one('res.currency',string="Currency")
    total_amount = fields.Float(string="Total Amount",compute="_compute_total_amount")
    state = fields.Selection([('draft','Draft'),
                              ('rent','Rent'),
                              ('returned','Returned'),
                              ('partially_invoiced','Partially Invoiced'),
                              ('invoiced','Invoiced'),
                              ('canceled','Canceled')],string="State",default='draft')

    bill_ids = fields.One2many('account.move', 'rental_order_id', string='Bills')
    bill_count = fields.Integer(string='Bill Count', compute='_compute_bill_count')
    amount_to_invoice = fields.Float(string="Amount to Invoice")


    @api.model_create_multi
    def create(self, vals_list):
        res = super(RentalOrder, self).create(vals_list)
        for rec in res:
            rec.rental_number = self.env['ir.sequence'].next_by_code('rental.order.sequence')
        return res

    @api.onchange('rent_start_date','rent_end_date')
    def _onchange_rental_dates(self):
        if self.rent_start_date and self.rent_end_date and self.rent_start_date > self.rent_end_date:
            raise ValidationError('Start Date cannot be greater than End Date')

    @api.depends('rental_order_line_ids','rent_start_date', 'rent_end_date')
    def _compute_total_amount(self):
        for rec in self:
            rec.total_amount = relativedelta(rec.rent_end_date,rec.rent_start_date).days * sum(rec.rental_order_line_ids.mapped('total_amount'))

    def generate_bill(self):
        return {
            'name': 'Bill',
            'type': 'ir.actions.act_window',
            'res_model': 'wizard.invoice.rental.orders',
            'view_mode': 'form',
            'context': {'default_total_rent_amount': self.total_amount,'default_rental_order_id': self.id,'default_amount_to_invoice': self.amount_to_invoice},
            'target': 'new',
        }

    @api.depends('bill_ids')
    def _compute_bill_count(self):
        for record in self:
            record.bill_count = len(record.bill_ids)

    def view_bills(self):
        return {
            'name': 'Bills',
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'domain': [('rental_order_id', '=', self.id)],
            'target': 'current',
        }

    def order_state_rent(self):
        self.state = 'rent'

    def order_state_returned(self):
        self.state = 'returned'

    def order_state_partially_invoiced(self):
        self.generate_bill()
        self.state = 'partially_invoiced'

    def order_state_invoiced(self):
        self.generate_bill()
        self.state = 'invoiced'

    def order_state_canceled(self):
        self.state = 'canceled'


