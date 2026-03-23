from odoo import models, fields,api,_
from odoo.exceptions import ValidationError


class RentalOrder(models.Model):
    _name = 'rental.order'
    _description = 'Rental Order'
    _rec_name = 'rental_id'

    rental_id = fields.Char(string='Rental Order ID',readonly=True)
    customer_id = fields.Many2one('res.partner', string='Customer',required=True)
    start_date = fields.Date(string='Start Date',required=True)
    end_date = fields.Date(string='End Date',required=True)
    total = fields.Float(string='Total',compute='_compute_total')
    rental_order_line_ids = fields.One2many('rental.order.lines', 'order_id', string='Rental Order Lines')
    state = fields.Selection([('draft', 'Draft'), ('rent', 'Rent'), ('returned', 'Returned'), ('invoiced', 'Invoiced'),
                              ('partially_invoiced', 'Partially Invoice'), ('cancelled', 'Cancelled')],default='draft')
    days = fields.Integer(string='Days',compute='_compute_days',store=True)

    @api.model
    def default_get(self, fields):
        defaults = super(RentalOrder, self).default_get(fields)
        if defaults.get('rental_id', 'New') == 'New':
            defaults['rental_id'] = self.env['ir.sequence'].next_by_code('order.sequence') or 'New'

        return defaults

    @api.onchange('start_date')
    def _onchange_start_date(self):
        for rec in self:
            if rec.start_date and rec.end_date and rec.end_date < rec.start_date:
                rec.start_date = False
                raise ValidationError(_('start date must be less than end date'))

    @api.onchange('end_date')
    def _onchange_end_date(self):
        for rec in self:
            if rec.end_date and rec.start_date and rec.start_date > rec.end_date:
                rec.end_date = False
                raise ValidationError(_('end date must be grater than start date'))


    def rent_state(self):
        self.write({'state':'rent'})

    def return_state(self):
        self.write({'state':'returned'})

    def cancel_state(self):
        self.write({'state':'cancelled'})

    def invoice_state(self):
        self.write({'state':'invoiced'})

    @api.depends('rental_order_line_ids.total_rent')
    def _compute_total(self):
        for rec in self:
            rec.total = 0
            for line in rec.rental_order_line_ids:
                rec.total += line.total_rent

    @api.depends('start_date', 'end_date')
    def _compute_days(self):
        for rec in self:
            if rec.start_date and rec.end_date:
                diff = abs(rec.start_date - rec.end_date)
                rec.days = diff.total_seconds() // (60 * 60 * 24)
