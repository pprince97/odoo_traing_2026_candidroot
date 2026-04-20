from odoo import api, fields, models
from odoo.exceptions import ValidationError

class VehicleBooking(models.Model):
    _name = "vehicle.booking"
    _description = "Vehicle Booking"
    _rec_name = 'customer_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    customer_id = fields.Many2one('res.partner',string="Customer",required=True, tracking = True)
    booking_line_ids = fields.One2many('vehicle.booking.line','booking_id',string="Booking Lines")
    rent_date = fields.Date(string="Rent Date",required=True)
    return_date = fields.Date(string="Return Date",required=True)
    trip_place = fields.Char(string="Trip Place",required=True)
    no_of_days = fields.Integer(string="No of Days",compute='_compute_no_of_days',store=True)
    state = fields.Selection([('draft','Draft'),('inquiry','Inquiry'),('approved','Approved'),('on_going','On Going'),('completed','Completed'),('paid','Paid'),('cancelled','Cancelled')],string="State",default='inquiry')
    damage_description = fields.Char(string="Damage Description")
    damage_charges = fields.Float(string="Damage Charges")
    total_kms = fields.Float(string="Total Kms",compute='_compute_total_kms',store=True)
    total_cost = fields.Float(string="Total Cost",compute='_compute_total_cost',store=True)
    invoice_id =fields.Many2one('account.move',string="Invoice")

    def state_approved(self):
        self.state = 'approved'
    def state_on_going(self):
        self.state = 'on_going'
    def state_completed(self):
        for line in self.booking_line_ids:
            line.vehicle_id.status = 'available'
            line.driver_id.status = True
        self.state = 'completed'
    def state_cancelled(self):
        for line in self.booking_line_ids:
            line.vehicle_id.status = 'available'
            line.driver_id.status = True
        self.state = 'cancelled'

    def state_paid(self):
        res = self.env['account.move'].with_context(
            {'default_move_type': 'out_invoice'}).create(
            {'partner_id': self.customer_id.id, 'invoice_date': fields.Date.today()})
        for line in self.booking_line_ids:
            self.env['account.move.line'].create(
                {'move_id': res.id,'product_id': line.vehicle_id.id, 'price_unit': line.cost})
            self.env['account.move.line'].create(
                {'move_id': res.id, 'name':f"{line.vehicle_id.name} {line.driver_id.name}", 'price_unit': (line.driver_id.driver_per_day_rate * self.no_of_days)})
            if line.adjusted_cost:
                self.env['account.move.line'].create(
                    {'move_id': res.id, 'name':f"{line.vehicle_id.name} adjusted", 'product_id': line.vehicle_id.id, 'price_unit': line.adjusted_cost})
        if self.damage_charges:
            self.env['account.move.line'].create(
                {'move_id': res.id, 'name':"damage charges", 'price_unit': self.damage_charges})
        res.update({'state': 'posted'})
        self.invoice_id = res.id
        self.state = 'paid'

    def state_print(self):
        return self.env.ref('car_rental_management_jui.action_report_booking').report_action(self.id)

    @api.onchange('rent_date')
    def _onchange_rent_date(self):
        for rec in self:
            if rec.rent_date and rec.return_date:
                if rec.rent_date > rec.return_date:
                    raise ValidationError("rent date cannot be greater than return date")

    @api.onchange('return_date')
    def _onchange_return_date(self):
        self._onchange_rent_date()

    @api.depends('rent_date','return_date')
    def _compute_no_of_days(self):
        for rec in self:
            if rec.rent_date and rec.return_date:
                rec.no_of_days = (rec.return_date - rec.rent_date).days

    @api.depends('booking_line_ids')
    def _compute_total_kms(self):
        for rec in self:
            rec.total_kms = 0
            if rec.booking_line_ids:
                for line in rec.booking_line_ids:
                    rec.total_kms += line.total_km

    @api.depends('booking_line_ids')
    def _compute_total_cost(self):
        for rec in self:
            rec.total_cost = 0
            if rec.booking_line_ids:
                for line in rec.booking_line_ids:
                    rec.total_cost += line.total_cost


    def create(self, vals):
        res = super(VehicleBooking, self).create(vals)
        for rec in res:
            if rec.booking_line_ids:
                for line in rec.booking_line_ids:
                    line.vehicle_id.status = 'booked'
                    line.driver_id.status = False
        return res

    def unlink(self):
        for rec in self:
            for line in rec.booking_line_ids:
                line.vehicle_id.status = 'available'
                line.driver_id.status = True
            res=super().unlink()
            return res
