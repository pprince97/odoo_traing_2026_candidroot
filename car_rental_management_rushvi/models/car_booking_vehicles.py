from odoo import api, fields, models, tools

class CarBookingVehicles(models.Model):
    _name = 'car.rent.booking.vehicles'
    _description = 'Booking Vehicles'

    vehicle_id = fields.Many2one('product.product', string='Vehicle',required=True)
    driver_id = fields.Many2one('res.partner',string='Driver')
    per_km_cost = fields.Float('Per KM Cost')
    trip_start_kms = fields.Integer(string="Trip Start km")
    trip_end_kms = fields.Integer(string="Trip End km")
    total_kms = fields.Float(string="Total Trip kms",compute='compute_total_kms',store=True)
    total_min_kms = fields.Float(string="Total Min kms",compute='compute_total_min_kms',store=True)
    booking_id = fields.Many2one('car.rent.booking', string='Booking')
    total_cost = fields.Float('Total Amount')

    # allowed_cars = fields.Many2many('product.product', string="Allowed Cars",compute="_compute_allowed_cars",store=True,readonly=False  )

    @api.depends('trip_start_kms', 'trip_end_kms')
    def compute_total_kms(self):
        for rec in self:
            if rec.trip_start_kms and rec.trip_end_kms:
                rec.total_kms = rec.trip_end_kms - rec.trip_start_kms
            else:
                rec.total_kms = 0

    @api.depends('booking_id', 'vehicle_id', 'booking_id.trip_start_date', 'booking_id.trip_end_date')
    def compute_total_min_kms(self):
        for rec in self:
            if rec.booking_id.trip_start_date and rec.booking_id.trip_end_date:
                rec.total_min_kms = (rec.booking_id.trip_end_date - rec.booking_id.trip_start_date).days * rec.vehicle_id.per_day_km
            else:
                rec.total_min_kms = 0

    @api.onchange('vehicle_id','total_kms')
    def _onchange_vehicle_id(self):
        if self.vehicle_id:
            self.per_km_cost = self.vehicle_id.cost_per_km
            if self.total_kms < self.total_min_kms:
                self.total_cost = self.per_km_cost * self.total_min_kms
            else:
                self.total_cost = self.per_km_cost * self.total_kms
        else:
            self.per_km_cost = 0
            self.total_cost = 0

    @api.onchange('vehicle_id','trip_start_kms')
    def onchange_vehicle_id_warning(self):
        latest_record = self.env['car.rent.maintenance'].search([('vehicle_id','=',self.vehicle_id.id)], order='arrival_date desc', limit=1)

        if self.trip_start_kms - latest_record.current_kms > self.vehicle_id.service_per_km:
            self.env['bus.bus']._sendone(self.env.user.partner_id, 'simple_notification', {
                'type': 'warning',
                'title': "Important Note",
                'message': f"Selected Car {self.vehicle_id.name} needs Maintainence .",
                'sticky': True,
            })

    # @api.depends('booking_id', 'booking_id.trip_start_date', 'booking_id.trip_end_date')
    # def _compute_allowed_cars(self):
    #     cars = self.env['product.product'].search([('vehicle_code','ilike','V%')])
    #     for record in self:
    #         if not record.booking_id:
    #             record.allowed_cars = self.env['product.product']
    #             continue
    #         else:
    #
    #
    #
    #
    #
    #
    #         busy_tasks = record.project_id.task_ids.filtered(
    #             lambda t: t.stage_id.id not in done_invoice_stage_ids
    #         )
    #         busy_assignee_ids = busy_tasks.mapped('assignee_ids').ids
    #         all_possible_assignees = record.project_id.mapped('assignee_ids')
    #         record.allowed_assignees = all_possible_assignees.filtered(
    #             lambda u: u.id not in busy_assignee_ids
    #         )