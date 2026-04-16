from pygments.styles import default

from odoo import api, fields, models

class Cars(models.Model):
    _inherit = "product.product"

    vehicle_code = fields.Char(string="Vehicle Code")
    vehicle_type = fields.Selection([('sedan','Sedan'),('suv','SUV'),('bus','Bus')],string="Vehicle Type")
    cost_per_km = fields.Float(string="Cost Per km")
    status = fields.Selection([('available','Available'),('booked','Booked'),('maintenance','Maintenance')],string="Status",default="available")
    service_per_km = fields.Integer(string="Service Per km")
    per_day_km = fields.Integer(string="Per Day km")
    maintenance_id = fields.Many2one('car.rent.maintenance',string="Maintenance Items")
    maintenance_count = fields.Integer(string="Maintenance Counts",compute='compute_maintenance_id')

    def status_available(self):
        self.status = 'available'

    def status_booked(self):
        self.status = 'booked'

    def status_maintenance(self):
        self.status = 'maintenance'

    @api.model_create_multi
    def create(self, vals_list):
        res = super(Cars, self).create(vals_list)
        for car in res:
            if car.categ_id.name == 'Vehicle':
                car.vehicle_code = self.env['ir.sequence'].next_by_code('vehicle.seq') or 'New'
        return res

    def view_maintenance_requests(self):
        return {
            'name': 'Maintenance',
            'type': 'ir.actions.act_window',
            'res_model': 'car.rent.maintenance',
            'view_mode': 'list,form',
            'domain': [('vehicle_id', '=', self.id)],
            'target': 'current',
        }

    def compute_maintenance_id(self):
        self.maintenance_count = self.env['car.rent.maintenance'].search_count([('vehicle_id','=',self.id)])

    def create_maintenance_request(self):
        return {
            'name': 'Maintenance Request',
            'type': 'ir.actions.act_window',
            'res_model': 'car.rent.maintenance',
            'view_mode': 'form',
            'domain': [('vehicle_id', '=', self.id)],
            'context': {'default_vehicle_id': self.id},
            'target': 'new',
        }