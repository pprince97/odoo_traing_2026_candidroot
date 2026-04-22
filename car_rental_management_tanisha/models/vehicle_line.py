from odoo import api, fields, models, _, Command
from odoo.exceptions import ValidationError


class VehicleLine(models.Model):
    _name = 'vehicle.line'
    _description = 'Vehicle Line'

    booking_id = fields.Many2one(comodel_name='rental.booking', string='Booking')
    vehicles = fields.Many2many(comodel_name='product.product',relation='booking_product_rel', column1='booking_id', column2='product_id',related='booking_id.vehicles')
    vehicle_id = fields.Many2one(comodel_name='product.product', string='Name')
    start_trip_km = fields.Integer(string='Start Trip KM')
    end_trip_km = fields.Integer(string='End Trip KM')
    drivers = fields.Many2many(comodel_name='res.partner',relation='booking_partner_rel', column1='booking_id', column2='partner_id',related='booking_id.drivers')
    driver_id = fields.Many2one(comodel_name='res.partner', string='Driver')
    currency_id = fields.Many2one(related='booking_id.currency_id')
    per_km_cost = fields.Monetary(related='vehicle_id.cost_per_km',store=True, readonly=True,currency_field='currency_id',string='Cost per KM')
    total_km = fields.Integer(string='Trip KM',compute='_compute_total_km',store=True)
    adjustment_km = fields.Integer(string='Adjustment KM',compute='_compute_adjustment_km',store=True)
    sub_cost = fields.Monetary(string='Sub Cost',store=True,currency_field='currency_id',compute='_compute_sub_cost')

    @api.depends('start_trip_km','end_trip_km')
    def _compute_total_km(self):
        for vehicle in self:
            if vehicle.start_trip_km or vehicle.end_trip_km:
                km_diff = vehicle.end_trip_km-vehicle.start_trip_km
                if km_diff > 0:
                    vehicle.total_km = km_diff
                else:
                    raise ValidationError(_("Start trip KM must be less than End trip KM!!!!!!"))
            else:
                vehicle.total_km = 0

    @api.depends('vehicle_id','start_trip_km','end_trip_km')
    def _compute_adjustment_km(self):
        for vehicle in self:
            if vehicle.total_km < vehicle.vehicle_id.per_day_km:
                vehicle.adjustment_km = vehicle.vehicle_id.per_day_km-vehicle.total_km
            else:
                vehicle.adjustment_km = 0

    @api.depends('adjustment_km','total_km','driver_id')
    def _compute_sub_cost(self):
        for vehicle in self:
            vehicle.sub_cost = ((vehicle.total_km+vehicle.adjustment_km) * vehicle.per_km_cost) + vehicle.driver_id.per_day_rate
