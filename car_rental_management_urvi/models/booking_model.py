from odoo import fields, models, api, Command
from odoo.fields import Domain


class Booking(models.Model):
    _name = 'car.rental.booking'
    _description = 'Car Rental Booking'
    _rec_name = 'customer_id'

    customer_id = fields.Many2one('res.partner', string='Customer',required=True)
    customer_phone = fields.Char(string='Customer Mobile', related='customer_id.phone')
    customer_email = fields.Char(string='Customer Email', related='customer_id.email')
    driver_id = fields.Many2one('res.partner', string='Driver',required=True)
    driver_per_day_rate = fields.Float(string='Driver Cost per Km', related='driver_id.per_day_rate')
    booking_lines = fields.One2many('car.rental.booking.lines', 'booking_id', 'Booking Lines')
    start_date = fields.Date(string='Start Date',required=True)
    end_date = fields.Date(string='End Date',required=True)
    trip_details = fields.Text(string='Trip Details')
    state = fields.Selection(
        [('draft', 'Draft'), ('inquiry', 'Inquiry'), ('approved', 'Approved'), ('on_going', 'On Going'),
         ('completed', 'Completed'), ('paid', 'Paid'), ('cancelled', 'Cancelled')], string='State')
    damage_description = fields.Text(string='Damage Description')
    damage_cost = fields.Float(string='Damage Cost')
    total_cost = fields.Float(string='Total Cost', compute='_compute_total_cost', store=True)
    days = fields.Integer(string='Days', compute='_compute_days', store=True)
    available_vehicles = fields.Many2many('product.product', 'booking_vehicle_rel', 'booking_id', 'vehicle_id',
                                          compute='_compute_available_vehicles')

    def inquiry_state(self):
        self.state = 'inquiry'

    def approved_state(self):
        self.state = 'approved'

    def cancelled_state(self):
        self.state = 'cancelled'

    def completed_state(self):
        self.state = 'completed'
        self.driver_id.status = 'available'
        for i in self.booking_lines:
            km = i.end_km - i.start_km
            i.vehicle_id.trip_km += km
            i.vehicle_id.status = 'available'

    def on_going_state(self):
        self.state = 'on_going'
        self.driver_id.status = 'not_available'
        for i in self.booking_lines:
            i.vehicle_id.status = 'booked'

    def generate_bill(self):
        self.state = 'paid'

    @api.depends('start_date', 'end_date')
    def _compute_days(self):
        for rec in self:
            if rec.start_date and rec.end_date:
                diff = abs(rec.start_date - rec.end_date)
                rec.days = diff.total_seconds() // (60 * 60 * 24)
                self._compute_available_vehicles()

    @api.depends('days', 'damage_cost', 'driver_id', 'booking_lines.cost')
    def _compute_total_cost(self):
        for rec in self:
            rec.total_cost = rec.driver_per_day_rate * rec.days + rec.damage_cost
            for i in rec.booking_lines:
                rec.total_cost += i.cost

    @api.depends('start_date', 'end_date')
    def _compute_available_vehicles(self):
        if self.start_date and self.end_date:
            domain = Domain.OR([Domain([('start_date', '<=', self.start_date),
                                        ('end_date', '>=', self.start_date)]),
                                Domain([('start_date', '<=', self.start_date),
                                        ('end_date', '>=', self.start_date)])])
            domain &= Domain([('state', 'in', ['approved', 'inquiry', 'on_going']),('id','!=',self.id)])
            id_s1 = self.env['car.rental.booking'].search(domain).booking_lines.vehicle_id.ids
            id_s2 = self.env['product.product'].search([('type','=','vehicle')]).ids
            self.write({'available_vehicles': [
                Command.set(list(set(id_s2) - set(id_s1)))]})
