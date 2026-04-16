from pygments.lexer import default

from odoo import api, fields, models
from datetime import date
from datetime import datetime
from odoo.exceptions import ValidationError
from odoo.fields import Many2one


class Booking(models.Model):
    _name = "car.booking"
    _description = "Booking"
    _rec_name = 'customer_id'
    company_id = fields.Many2one('res.company')

    # customer_name = fields.Char(string="Customer Name")
    customer_id = fields.Many2one('res.partner' , string="Customer")
    customer_aadhar_number = fields.Char(string="Customer Aadhar Number")

    # product_car_ids = fields.Many2many('product.product', string="Products Car")
    # driver_ids = fields.Many2many('res.partner', string="Drivers")

    trip_details = fields.Text(string="Trip Details")

    trip_start_date = fields.Date(string="Trip Start Date")
    trip_end_date = fields.Date(string="Trip End Date")
    days = fields.Integer(string="Days",compute='_compute_trip_days', default=1)

    damage_details = fields.Text(string="Damage Details")
    damage_charges = fields.Float(string="Damage Charges")

    total_cost = fields.Float(string="Total Cost")

    record_booking_ids = fields.One2many('record.booking','booking_id',string="Record Bookings")
    # driver_id = fields.Many2one(related='record_booking_ids.driver_id',string="Drivers")
    # print("driver ids ------ >",driver_id)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('inquiry', 'Inquiry'),
        ('approved', 'Approved'),
        ('on_going', 'On-going'),
        ('completed', 'Completed'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ],
        default='inquiry',
        string="State",
    )

    def inquiry_state(self):
        self.update({'state': 'inquiry'})

    def approved_state(self):
        self.update({'state': 'approved'})

    def on_going_state(self):
        for record in self.record_booking_ids:
            record.product_car_id.update({'status': 'booked'})
            record.driver_id.update({'status': 'booked'})
        self.update({'state': 'on_going'})

    def completed_state(self):
        for record in self.record_booking_ids:
            record.product_car_id.update({'status': 'available'})
            record.driver_id.update({'status': 'available'})
        self.update({'state': 'completed'})

    def paid_state(self):
        l = []
        self.total_cost = 0
        for record in self.record_booking_ids:
            for car in record.product_car_id:
                if record.trip_km > car.min_km_per_day :
                    self.total_cost += record.trip_km * car.cost_per_km * self.days
                    l.append((0, 0, {'name': car.name, 'quantity': 1, 'price_unit': record.trip_km * car.cost_per_km * self.days}))
                else:
                    total = car.min_km_per_day * car.cost_per_km * self.days
                    self.total_cost += total
                    car_cost = record.trip_km * car.cost_per_km * self.days
                    extra_cost = total - car_cost
                    l.append((0, 0, {'name': car.name, 'quantity': 1, 'price_unit': car_cost}))
                    l.append((0, 0, {'name': "adjustment kilometers", 'quantity': 1, 'price_unit': extra_cost}))

            for driver in record.driver_id:
                self.total_cost += driver.per_day_rate * self.days
                l.append((0, 0, {'name': driver.name, 'quantity': 1, 'price_unit': driver.per_day_rate * self.days}))
                # print('car.name>>>>>>>>>>.', car.name)
                # print('car.name>>>>>>>>>>.', car.cost_per_km)
                # print('car.name>>>>>>>>>>.', car.service_per_km)
                # print('car.name>>>>>>>>>>.', car.min_km_per_day)
            #     print('-------------------')
            # print('record.trip_start_km>>>>>>>>>>.', record.trip_start_km)
            # print('record.trip_end_km>>>>>>>>>>.', record.trip_end_km)
            # print('record.trip_km>>>>>>>>>>.', record.trip_km)

        if self.damage_charges:
            self.total_cost += self.damage_charges
            l.append((0, 0, {'name': "damage charges", 'quantity': 1, 'price_unit': self.damage_charges}))
        print("l--------->",l)
        print("self.total_cost--------->",self.total_cost)
        res = self.env['account.move'].with_context({'default_move_type': 'in_invoice'}).create(
            {'partner_id': self.company_id.id, 'invoice_date': fields.Date.today(), 'invoice_line_ids': l})
        self.update({'state': 'paid'})

    def cancelled_state(self):
        self.update({'state': 'cancelled'})

    def draft_state(self):
        self.update({'state': 'draft'})

    def _compute_trip_days(self):
        for rec in self:
            if rec.trip_start_date and rec.trip_end_date:
                trip = rec.trip_end_date - rec.trip_start_date
                print('trip ----->   ',trip)
                rec.days = trip.days
            else:
                rec.days = 0

    #             This is for Available Car
    # def write(self, vals):
    #     for task in self:
    #         old_users = task.record_booking_ids
    #     res = super().write(vals)
    #     if 'record_booking_ids' in vals:
    #         for task in self:
    #             new_users = task.record_booking_ids
    #             print(new_users, ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    #             added_users = new_users - old_users
    #             removed_users = old_users - new_users
    #             print(added_users, removed_users, ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    #             # mark added users unavailable
    #             for user in added_users:
    #                 user.available = False
    #             # mark removed users available
    #             for user in removed_users:
    #                 user.available = True
    #     return res

