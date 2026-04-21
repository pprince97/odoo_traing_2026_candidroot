from odoo import api, fields, models, Command
from odoo.exceptions import ValidationError
from odoo.fields import Domain
import logging

logger = logging.getLogger('odoo.registry')
class VehicleBookingLine(models.Model):
    _name = "vehicle.booking.line"
    _description = "Vehicle Booking Line"
    _rec_name = 'vehicle_id'

    vehicle_id = fields.Many2one('product.product',string="Vehicle")
    available_vehicles = fields.Many2many('product.product','product_booking_rel','booking_line_id','booking_id',string="Available Vehicles",compute='_compute_available_vehicles')
    start_km = fields.Float(string="Start Km")
    end_km = fields.Float(string="End Km")
    total_km = fields.Float(string="Total Km",compute="_compute_total_km",store=True)
    driver_id = fields.Many2one('res.partner',string="Driver")
    available_driver = fields.Many2many('res.partner','res_partner_booking_rel','booking_line_id','booking_id',string="Available Drivers",compute='_compute_available_drivers')
    booking_id = fields.Many2one('vehicle.booking',string="Booking")
    total_cost = fields.Float(string="Total Cost",compute="_compute_total_cost",store=True)
    cost = fields.Float(string="Total Cost")
    adjusted_cost = fields.Float(string="Adjusted Cost")

    @api.depends('booking_id.rent_date', 'booking_id.return_date')
    def _compute_available_vehicles(self):
        if self.booking_id.rent_date and self.booking_id.return_date:
            domain = Domain.OR([Domain([('rent_date', '<=', self.booking_id.rent_date),
                                        ('return_date', '>=', self.booking_id.rent_date)]),
                                Domain([('rent_date', '<=', self.booking_id.return_date),
                                        ('return_date', '>=', self.booking_id.return_date)])])
            domain &= Domain([('state', 'in', ['draft','approved', 'inquiry', 'on_going']), ('id', '!=', self.booking_id.id)])
            id_s1 = self.env['vehicle.booking'].search(domain).booking_line_ids.vehicle_id.ids
            id_s2 = self.env['product.product'].search([('is_vehicle', '=', True),('id','not in',self.booking_id.booking_line_ids.vehicle_id.ids)]).ids
            self.write({'available_vehicles': [
                Command.set(list(set(id_s2) - set(id_s1)))]})
        else:
            id_s1 = self.env['product.product'].search([('is_vehicle', '=', True),('status','in',['available']),('id','not in',self.booking_id.booking_line_ids.vehicle_id.ids)]).ids
            self.write({'available_vehicles': [
                Command.set(list(set(id_s1)))]})

    @api.depends('booking_id.rent_date', 'booking_id.return_date')
    def _compute_available_drivers(self):
        if self.booking_id.rent_date and self.booking_id.return_date:
            domain = Domain.OR([Domain([('rent_date', '<=', self.booking_id.rent_date),
                                        ('return_date', '>=', self.booking_id.rent_date)]),
                                Domain([('rent_date', '<=', self.booking_id.return_date),
                                        ('return_date', '>=', self.booking_id.return_date)])])
            domain &= Domain([('state', 'in', ['draft', 'approved', 'inquiry', 'on_going']), ('id', '!=', self.booking_id.id)])
            id_s1 = self.env['vehicle.booking'].search(domain).booking_line_ids.driver_id.ids
            id_s2 = self.env['res.partner'].search([('is_driver', '=', True), ('id', 'not in', self.booking_id.booking_line_ids.driver_id.ids)]).ids
            self.write({'available_driver': [
                Command.set(list(set(id_s2) - set(id_s1)))]})
        else:
            id_s1 = self.env['res.partner'].search([('is_driver', '=', True), ('status', '=', True),('id', 'not in',self.booking_id.booking_line_ids.driver_id.ids)]).ids
            self.write({'available_driver': [
                Command.set(list(set(id_s1)))]})

    @api.onchange('vehicle_id','start_km')
    def _onchange_vehicle_id(self):
        for rec in self:
            if rec.vehicle_id and rec.vehicle_id.maintenance_ids.ids:
                maintenance = self.env['vehicle.maintenance'].browse(rec.vehicle_id.maintenance_ids.ids[-1])
                if rec.start_km - maintenance.current_km > rec.vehicle_id.service_per_km:
                    logger.warning(f"this vehicle's service is pending")
                    self.env['bus.bus']._sendone(self.env.user.partner_id, 'simple_notification', {
                        'type': 'warning',
                        'title': "Important Note",
                        'message': f"Selected vehicle {self.vehicle_id.name} needs Maintenance .",
                        'sticky': True,
                    })

    @api.onchange('start_km')
    def _onchange_start_km(self):
        for rec in self:
            if rec.start_km < 0:
                raise ValidationError("start km cannot be negative")

    @api.depends('start_km', 'end_km')
    def _compute_total_km(self):
        for rec in self:
            if (rec.start_km != None) and rec.end_km:
                if rec.start_km < rec.end_km:
                    rec.total_km = (rec.end_km - rec.start_km)
                else:
                    raise ValidationError("start km must be less than end km")

    @api.depends('total_km','booking_id.no_of_days','vehicle_id')
    def _compute_total_cost(self):
        for rec in self:
            if rec.total_km:
                estimated_km = rec.booking_id.no_of_days * rec.vehicle_id.per_day_km
                if rec.total_km < estimated_km:
                    rec.total_cost = estimated_km * rec.vehicle_id.cost_per_km
                    rec.cost = rec.total_km * rec.vehicle_id.cost_per_km
                    rec.adjusted_cost = (estimated_km - rec.total_km) * rec.vehicle_id.cost_per_km
                else:
                    rec.total_cost = rec.total_km * rec.vehicle_id.cost_per_km
                    rec.adjusted_cost = 0
                    rec.cost = rec.total_km * rec.vehicle_id.cost_per_km
