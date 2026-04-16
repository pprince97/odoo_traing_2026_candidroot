from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

class CarBooking(models.Model):
    _name = 'car.rent.booking'
    _description = 'Car Booking'
    _rec_name='serial_number'
    _inherit = ['mail.thread', 'portal.mixin']

    serial_number = fields.Char(string='Serial Number')
    customer_id = fields.Many2one('res.partner', string='Customer', required=True)
    booking_vehicle_ids = fields.One2many('car.rent.booking.vehicles', 'booking_id', string='Vehicles')
    trip_start_date = fields.Datetime(string='Start Date', required=True)
    trip_end_date = fields.Datetime(string='End Date', required=True)
    trip_details = fields.Text(string='Details', required=True)
    state = fields.Selection([('draft', 'Draft'),
                              ('inquiry', 'Inquiry'),
                              ('approved', 'Approved'),
                              ('on_going', 'On Going'),
                              ('completed', 'Completed'),
                              ('paid', 'Paid'),
                              ('canceled', 'Canceled')],
                             default='inquiry',
                             string='Status')
    total_cost = fields.Float(string='Total Cost', compute='_compute_total_cost', store=True)
    damage_description = fields.Text(string='Damage Description')
    damage_cost = fields.Float(string='Damage Cost', default=0)
    invoice_id = fields.Many2one('account.move', string='Invoice')


    @api.model_create_multi
    def create(self, vals_list):
        res = super(CarBooking, self).create(vals_list)
        for rec in res:
            rec.serial_number = self.env['ir.sequence'].next_by_code('booking.seq') or 'New'
        return res

    def state_inquiry(self):
        self.state = 'inquiry'

    def state_canceled(self):
        self.state = 'canceled'

    def state_completed(self):
        for rec in self.booking_vehicle_ids:
            rec.vehicle_id.status = 'available'
            rec.driver_id.status = 'available'
        self.total_cost = sum(self.booking_vehicle_ids.mapped('total_cost')) + self.damage_cost
        self.state = 'completed'

    def state_paid(self):
        self.state = 'paid'

    def state_on_going(self):
        for rec in self.booking_vehicle_ids:
            rec.vehicle_id.status = 'booked'
            rec.driver_id.status = 'on_trip'
        self.state = 'on_going'

    def state_approved(self):
        self.state = 'approved'

    @api.onchange('damage_cost')
    def onchange_damage_cost(self):
        self.total_cost = sum(self.booking_vehicle_ids.mapped('total_cost')) + self.damage_cost

    @api.onchange('trip_start_date', 'trip_end_date')
    def onchange_trip_start_date(self):
        if self.trip_start_date and self.trip_end_date and self.trip_start_date > self.trip_end_date:
            raise ValidationError("Start Date can't be earlier than End Date")

    def generate_invoice(self):
        invoice_lines = []
        for task in self.booking_vehicle_ids:
            if task.total_kms < task.total_min_kms:
                invoice_lines.extend([(0, 0, {
                    'name': task.vehicle_id.name,
                    'quantity': task.total_kms,
                    'price_unit': task.per_km_cost,
                }), (0, 0, {
                    'name': task.vehicle_id.name + " Adjustment ",
                    'quantity': (task.total_min_kms - task.total_kms),
                    'price_unit': task.per_km_cost,
                }), (0, 0, {
                    'name': "Driver Cost: " + task.driver_id.name,
                    'quantity': (task.booking_id.trip_end_date - task.booking_id.trip_start_date).days,
                    'price_unit': task.driver_id.driver_per_day_rate,
                })])
            else:
                invoice_lines.extend([(0, 0, {
                    'name': task.vehicle_id.name,
                    'quantity': task.total_kms,
                    'price_unit': task.per_km_cost,
                }), (0, 0, {
                    'name': "Driver Cost: " + task.driver_id.name,
                    'quantity': (task.booking_id.trip_end_date - task.booking_id.trip_start_date).days,
                    'price_unit': task.driver_id.driver_per_day_rate,
                })])
        move = self.env['account.move'].create({
            'move_type': 'in_invoice',
            'partner_id': self.customer_id.id,
            'invoice_date': fields.Date.today(),
            'invoice_line_ids': invoice_lines,
        })
        move.write({
            'state': 'posted',
        })
        self.invoice_id = move.id

    def _get_report_base_filename(self):
        self.ensure_one()
        return f'{self.serial_number} {self.customer_id.name}'
