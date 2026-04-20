from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class VehicleLine(models.Model):
    _name = 'vehicle.line'
    _description = 'Vehicle Line'

    vehicle_id = fields.Many2one(comodel_name='product.product', string="Vehicle")
    start_trip_km = fields.Float(string='Start Trip KM')
    end_trip_km = fields.Float(string='End Trip KM')
    driver_id = fields.Many2one(comodel_name='res.partner', string='Driver')
    currency_id = fields.Many2one(comodel_name='res.currency', string="Foreign Currency")
    per_km_cost = fields.Monetary(related='vehicle_id.cost_per_km',store=True, readonly=True,currency_field='currency_id',string='Cost per KM')
    total_km = fields.Float(string='Trip KM',compute='_compute_total_km',store=True)
    booking_id = fields.Many2one(comodel_name='rental.booking', string='Booking')
    sub_cost = fields.Monetary(string='Sub Cost',store=True,currency_field='currency_id',compute='_compute_sub_cost')

    @api.depends('start_trip_km','end_trip_km')
    def _compute_total_km(self):
        for vehicle in self:
            if vehicle.start_trip_km and vehicle.end_trip_km:
                km_diff = vehicle.end_trip_km-vehicle.start_trip_km
                if km_diff > 0:
                    vehicle.total_km = km_diff
                else:
                    raise ValidationError(_("Start trip KM must be less than End trip KM!!!!!!"))

    @api.depends('total_km')
    def _compute_sub_cost(self):
        for vehicle in self:
            vehicle.sub_cost = vehicle.total_km * vehicle.per_km_cost
