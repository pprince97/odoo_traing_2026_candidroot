from odoo import fields, models


class FleetVehicleState(models.Model):
    _name = 'fleet.vehicle.state'
    _description = 'Vehicle State'
    _order = 'name asc'

    name = fields.Char(string='Status', required=True)


class FleetVehicle(models.Model):
    _name = 'fleet.vehicle'
    _description = 'Fleet Vehicle'
    _order = 'name asc'

    name = fields.Char(string='Vehicle Name', required=True)
    license_plate = fields.Char(string='License Plate')
    state_id = fields.Many2one('fleet.vehicle.state', string='Status')
    driver_id = fields.Many2one('res.partner', string='Driver')
