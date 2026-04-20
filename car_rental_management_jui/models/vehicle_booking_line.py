from odoo import api, fields, models, Command
from odoo.exceptions import ValidationError
import logging

logger = logging.getLogger('odoo.registry')
class VehicleBookingLine(models.Model):
    _name = "vehicle.booking.line"
    _description = "Vehicle Booking Line"
    _rec_name = 'vehicle_id'

    vehicle_id = fields.Many2one('product.product',string="Vehicle")
    start_km = fields.Float(string="Start Km")
    end_km = fields.Float(string="End Km")
    total_km = fields.Float(string="Total Km",compute="_compute_total_km",store=True)
    driver_id = fields.Many2one('res.partner',string="Driver")
    booking_id = fields.Many2one('vehicle.booking',string="Booking")
    booking_rent_date = fields.Date(string="Booking Return Date",related="booking_id.rent_date")
    total_cost = fields.Float(string="Total Cost",compute="_compute_total_cost",store=True)
    cost = fields.Float(string="Total Cost")
    adjusted_cost = fields.Float(string="Adjusted Cost")

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
