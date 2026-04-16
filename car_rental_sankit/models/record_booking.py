from odoo import api, fields, models

from odoo.exceptions import ValidationError


class RecordCar(models.Model):
    _name = 'record.booking'
    _description = 'Record Booking'
    _rec_name = 'product_car_id'

    product_car_id = fields.Many2one('product.product', string="Products Car")
    driver_id = fields.Many2one('res.partner', string="Drivers")
    trip_start_km = fields.Float(string="Trip Start Km")
    trip_end_km = fields.Float(string="Trip End Km")
    trip_km = fields.Float(string="Trip Km" , compute='_compute_trip_km')

    booking_id = fields.Many2one('car.booking', string="Booking")

    @api.depends('trip_start_km', 'trip_end_km','booking_id')
    def _compute_trip_km(self):
        for rec in self:
            if rec.trip_start_km and rec.trip_end_km and rec.trip_end_km >= rec.trip_start_km:
                rec.trip_km = rec.trip_end_km - rec.trip_start_km
            else:
                raise ValidationError("Trip End Km must be greater than Trip Start Km")


