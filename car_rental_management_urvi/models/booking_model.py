from odoo import fields, models, api, Command
from odoo.fields import Domain
from odoo.exceptions import ValidationError


class Booking(models.Model):
    _name = 'car.rental.booking'
    _description = 'Car Rental Booking'
    _rec_name = 'customer_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    customer_id = fields.Many2one('res.partner', string='Customer',required=True,tracking=True)
    customer_phone = fields.Char(string='Customer Mobile', related='customer_id.phone')
    customer_email = fields.Char(string='Customer Email', related='customer_id.email')
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
    available_vehicles = fields.Many2many('product.product', 'booking_vehicle_rel', 'booking_id', 'vehicle_id', compute='_compute_available_vehicles')
    available_drivers = fields.Many2many('res.partner', 'booking_partner_rel', 'booking_id', 'driver_id')
    invoice_id = fields.Many2one('account.move', string='Invoice')

    def inquiry_state(self):
        self.state = 'inquiry'

    def approved_state(self):
        self.state = 'approved'

    def cancelled_state(self):
        self.state = 'cancelled'

    def completed_state(self):
        self.state = 'completed'
        for i in self.booking_lines:
            km = i.end_km - i.start_km
            i.vehicle_id.trip_km += km
            i.vehicle_id.status = 'available'
            i.driver_id.status = 'available'

    def on_going_state(self):
        self.state = 'on_going'
        for i in self.booking_lines:
            i.vehicle_id.status = 'booked'
            i.driver_id.status = 'not_available'

    def generate_bill(self):
        invoice_lines = []
        for line in self.booking_lines:
            invoice_lines.append((0, 0, {
                'name': line.vehicle_id.name,
                'quantity': 1,
                'price_unit': line.cost,
            }))

        if self.damage_cost > 0:
            invoice_lines.append((0, 0, {
                'name': self.damage_description or "Damage Charges",
                'quantity': 1,
                'price_unit': self.damage_cost,
            }))

        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.customer_id.id,
            'invoice_date': fields.Date.today(),
            'state': 'draft',
            'invoice_line_ids': invoice_lines,
        })

        self.invoice_id = invoice.id

        self.state = 'paid'

        return {
            'name': 'Customer Invoice',
            'view_mode': 'form',
            'res_model': 'account.move',
            'res_id': invoice.id,
            'type': 'ir.actions.act_window',
        }

    @api.depends('start_date', 'end_date')
    def _compute_days(self):
        for rec in self:
            if rec.start_date and rec.end_date:
                diff = abs(rec.start_date - rec.end_date)
                rec.days = diff.total_seconds() // (60 * 60 * 24) + 1
                self._compute_available_vehicles()

    @api.depends('days', 'damage_cost', 'booking_lines.cost')
    def _compute_total_cost(self):
        for rec in self:
            rec.total_cost = rec.damage_cost
            for i in rec.booking_lines:
                rec.total_cost += i.cost

    @api.depends('start_date', 'end_date')
    def _compute_available_vehicles(self):
        if self.start_date and self.end_date:
            domain = Domain.OR([Domain([('start_date', '<=', self.start_date),
                                        ('end_date', '>=', self.start_date)]),
                                Domain([('start_date', '<=', self.end_date),
                                        ('end_date', '>=', self.end_date)])])
            domain &= Domain([('state', 'in', ['approved', 'inquiry', 'on_going']),('id','!=',self.id)])
            id_s1 = self.env['car.rental.booking'].search(domain).booking_lines.vehicle_id.ids
            id_s2 = self.env['product.product'].search([('type','=','vehicle'),('id','not in',self.booking_lines.vehicle_id.ids)]).ids
            self.write({'available_vehicles': [
                Command.set(list(set(id_s2) - set(id_s1)))]})
            id_d1 = self.env['car.rental.booking'].search(domain).booking_lines.driver_id.ids
            id_d2 = self.env['res.partner'].search([('is_driver','=',True),('id','not in',self.booking_lines.driver_id.ids)]).ids
            self.write({'available_drivers': [
                Command.set(list(set(id_d2) - set(id_d1)))]})

    @api.constrains('start_date')
    def _constrains_start_date(self):
        if self.start_date and self.start_date < fields.Date.today():
            raise ValidationError('Start Date cannot be in the past')
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValidationError('Start Date cannot be Greater than End Date')

    @api.constrains('end_date')
    def _constrains_end_date(self):
        if self.end_date and self.end_date < fields.Date.today():
            raise ValidationError('End Date cannot be in the past')
        if self.end_date and self.end_date and self.end_date < self.start_date:
            raise ValidationError('End Date cannot be Less than Start Date')