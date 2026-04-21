from odoo import fields,models,api,_
from odoo.exceptions import UserError


class BookingLines(models.Model):
    _name = 'car.rental.booking.lines'
    _description = 'Booking Lines'

    vehicle_id = fields.Many2one('product.product',string='Vehicle')
    start_km = fields.Integer(string='Start Km')
    end_km = fields.Integer(string='End Km')
    vehicle_per_day_cost = fields.Float(string='Cost/day',related='vehicle_id.lst_price')
    booking_id = fields.Many2one('car.rental.booking',string='Booking')
    km_per_day = fields.Float(string='Km/day',compute='_compute_km',store=True)
    required_km = fields.Integer(string='Required Km/day',related='vehicle_id.per_day_km')
    applicable_km = fields.Float(string='Applicable Km/day',compute='_compute_applicable_km',store=True)
    cost = fields.Float(string='Cost',compute='_compute_cost',store=True)
    available_vehicles_l = fields.Many2many('product.product', 'booking_vehicle_rel', 'booking_id', 'vehicle_id',
                                         related = 'booking_id.available_vehicles')
    available_driver_l = fields.Many2many('res.partner', 'booking_partner_rel', 'booking_id', 'driver_id',related = 'booking_id.available_drivers')
    driver_id = fields.Many2one('res.partner', string='Driver')
    driver_per_day_rate = fields.Float(string='Driver Cost per Km', related='driver_id.per_day_rate')

    @api.constrains('start_km')
    def _constrains_start_km(self):
        if not self.start_km >= 0:
            raise UserError(_('Start Km can not be negative'))

    @api.constrains('end_km')
    def _constrains_end_km(self):
        if self.end_km < 0 or self.end_km <= self.start_km:
            raise UserError(_('Enter Valid End km'))

    @api.onchange('vehicle_id')
    def _onchange_vehicle_id(self):
            if self.vehicle_id.required_maintenance:
                # return {'warning': {
                #     'message': (self.vehicle_id.name," Vehicle required Service")
                # }}
                self.env['bus.bus']._sendone(self.env.user.partner_id, 'simple_notification', {
                    'type': 'warning',
                    'title': "Important Note",
                    'message': f"Selected Car {self.vehicle_id.name} needs Maintainence .",
                    'sticky': True,
                })


    @api.depends('start_km','end_km','booking_id.days')
    def _compute_km(self):
        for rec in self:
            if rec.start_km!=rec.end_km and rec.booking_id.days:
                rec.km_per_day = (rec.end_km - rec.start_km)/ rec.booking_id.days

    @api.depends('km_per_day','required_km')
    def _compute_applicable_km(self):
        for rec in self:
            if rec.km_per_day < rec.required_km:
                rec.applicable_km = rec.required_km
            else:
                rec.applicable_km = rec.km_per_day

    @api.depends('applicable_km','vehicle_id','booking_id.days')
    def _compute_cost(self):
        for rec in self:
            if rec.applicable_km and rec.vehicle_per_day_cost and rec.booking_id.days:
                rec.cost = (rec.applicable_km * rec.vehicle_per_day_cost + rec.driver_per_day_rate)* rec.booking_id.days


