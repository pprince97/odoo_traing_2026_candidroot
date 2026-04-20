from odoo import api, fields, models

from odoo.exceptions import ValidationError


class RecordCar(models.Model):
    _name = 'record.booking'
    _description = 'Record Booking'
    _rec_name = 'product_car_id'

    forbidden_car_ids = fields.Many2many('product.product', compute='_compute_forbidden_resources')
    forbidden_driver_ids = fields.Many2many('res.partner', compute='_compute_forbidden_resources')


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

    @api.constrains('driver_id', 'booking_id')
    def _check_driver_overlap(self):
        """
        Constraint to prevent assigning the same driver to overlapping bookings.
        """
        for record in self:
            # 1. Skip if no driver or booking is assigned
            if not record.driver_id or not record.booking_id:
                continue

            # 2. Get dates from the parent booking model
            # Ensure the dates exist in the booking record
            start_date = record.booking_id.trip_start_date
            end_date = record.booking_id.trip_end_date

            if not start_date or not end_date:
                continue

            # 3. Search for OTHER records with the same driver that overlap
            # The logic:
            # ('id', '!=', record.id) -> Ignore the current record
            # ('driver_id', '=', record.driver_id.id) -> Same driver
            # ('booking_id.trip_start_date', '<', end_date) -> Existing booking starts before current ends
            # ('booking_id.trip_end_date', '>', start_date) -> Existing booking ends after current starts
            overlapping_driver = self.env['record.booking'].search([
                ('id', '!=', record.id),
                ('driver_id', '=', record.driver_id.id),
                ('booking_id.trip_start_date', '<', end_date),
                ('booking_id.trip_end_date', '>', start_date),
            ])
            print('overlapping_driver ----->  ',overlapping_driver)

            if overlapping_driver:
                raise ValidationError(f'The driver {record.driver_id.name} is already booked for another trip during this period ({start_date} to {end_date}).')

            overlapping_car = self.env['record.booking'].search([
                ('id', '!=', record.id),
                ('product_car_id', '=', record.product_car_id.id),
                ('booking_id.trip_start_date', '<', end_date),
                ('booking_id.trip_end_date', '>', start_date),
            ])
            print('overlapping_car ----->  ', overlapping_car)

            if overlapping_car:
                raise ValidationError(
                    f'The Car {record.product_car_id.name} is already booked for another trip during this period ({start_date} to {end_date}).')



    @api.depends('booking_id.trip_start_date', 'booking_id.trip_end_date')
    def _compute_forbidden_resources(self):
        for record in self:
            # 1. Default to empty lists
            forbidden_cars = []
            forbidden_drivers = []
            # 2. If dates are set, find overlapping bookings
            if record.booking_id.trip_start_date and record.booking_id.trip_end_date:
                start = record.booking_id.trip_start_date
                end = record.booking_id.trip_end_date
                # Search for all bookings that overlap with the current date range
                overlapping = self.env['record.booking'].search([
                    ('id', '!=', record.id),  # Exclude current record
                    ('booking_id.trip_start_date', '<', end),
                    ('booking_id.trip_end_date', '>', start),
                ])
                # print('overlapping ----->  ', overlapping)
                # 3. Collect the IDs of the busy cars and drivers
                forbidden_cars = overlapping.mapped('product_car_id.id')
                forbidden_drivers = overlapping.mapped('driver_id.id')
                # print('forbidden_cars ----->  ', forbidden_cars)
                # print('forbidden_drivers ----->  ', forbidden_drivers)
            # 4. Assign to the computed fields
            record.forbidden_car_ids = [(6, 0, forbidden_cars)]
            record.forbidden_driver_ids = [(6, 0, forbidden_drivers)]
            # print('record.forbidden_car_ids ----->  ', record.forbidden_car_ids)
            # print('record.forbidden_driver_ids ----->  ', record.forbidden_driver_ids)
