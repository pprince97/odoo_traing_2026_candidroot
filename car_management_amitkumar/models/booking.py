from odoo import fields, api, models
from odoo.exceptions import ValidationError


class BookingManagement(models.Model):
    _name = 'booking.management'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _description = 'Booking Management'

    customer_detail_ids = fields.Many2many('res.partner', string="Customer", tracking=True)
    vehicle_detail_ids = fields.Many2many('product.product', string="Vehicle", tracking=True)

    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")

    trip_detail = fields.Char(string="Trip Detail")

    states = fields.Selection([
        ('draft', 'Draft'),
        ('inquiry', 'Inquiry'),
        ('approved', 'Approved'),
        ('ongoing', 'On-going'),
        ('completed', 'Completed'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ],
        default='draft',
        string="Status"
    )

    start_km = fields.Float(string="Start KM")
    end_km = fields.Float(string="End KM")

    damage_description = fields.Text(string="Damage Description")
    damage_charge = fields.Float(string="Damage Charge")

    trip_km = fields.Float(string="Trip Total KM")
    km_cost = fields.Float(string="Per KM Cost", default=0.0)

    total_trip_cost = fields.Float(string="Total Trip Cost")
    issue_days = fields.Integer(string="Issued Days")

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            val['states'] = 'inquiry'

        res = super(BookingManagement, self).create(vals_list)
        return res

    # Km calculated
    @api.onchange('start_km', 'end_km')
    def km_calc(self):
        self.trip_km = self.end_km - self.start_km


    @api.onchange('customer_detail_ids')
    def onchange_customer_detail_ids(self):
        print("\n\nCustomer Name =======>", self.customer_detail_ids._origin, len(self.customer_detail_ids))

        for j in self.customer_detail_ids:
            print(j.name)
            print(j.driver_per_day_rate)


    @api.onchange('vehicle_detail_ids')
    def onchange_vehicle_details(self):
        print("\n\nVehicle Name =======>", self.vehicle_detail_ids._origin, len(self.vehicle_detail_ids))

        for rec in self:
            self.km_cost = sum(rec.vehicle_detail_ids.mapped('cost_per_km'))

        for i in self.vehicle_detail_ids:
            if i.status == 'maintenance':
                raise ValidationError('Vehicle Service is in maintenance mode!')


    # total cost
    @api.onchange('trip_km','km_cost')
    def calculate_total_cost(self):
        # customer_km = self.trip_km
        # car_default_km = self.vehicle_detail_ids.mapped('per_day_km')
        # total = car_default_km * self.issue_days
        #
        # if total > self.trip_km:
        #     self.total_trip_cost = total * self.km_cost
        # else:
        self.total_trip_cost = self.trip_km * self.km_cost



    # Count days
    @api.onchange('start_date', 'end_date')
    def _onchange_days(self):
        if self.start_date and self.end_date:
            if self.start_date > self.end_date:
                raise ValidationError("issue_date must be before return_date")
            else:
                res = ((self.end_date - self.start_date).total_seconds()) / 86400
                self.issue_days = res



    def action_draft(self):
        self.update({'states': 'draft'})

    def action_inquiry(self):
        self.update({'states': 'inquiry'})

    def action_approved(self):
        self.update({'states': 'approved'})

    def action_ongoing(self):
        self.update({'states': 'ongoing'})

    def action_cancelled(self):
        self.update({'states': 'cancelled'})

    def action_paid(self):
        self.update({'states': 'paid'})

    def action_completed(self):
        self.update({'states': 'completed'})
