from odoo import fields,models

class Maintenance(models.Model):
    _name = 'car.rental.maintenance'
    _description = 'Maintenance'
    _rec_name = 'vehicle_id'

    vehicle_id = fields.Many2one('product.product',string='Vehicle')
    current_km = fields.Integer(string='Current KM')
    arrival_date = fields.Date(string='Arrival Date',default=fields.Date.today(),readonly=True)
    dispatch_date = fields.Date(string='Dispatch Date',readonly=True)
    maintenance_lines = fields.One2many('car.rental.maintenance.lines','maintenance_id',string='Maintenance Lines')
    state = fields.Selection([('pending','Pending'),('in_process','In Process'),('completed','Completed'),('paid','Paid')],string='State',default='pending')
    total_cost = fields.Float(string='Total Cost',compute='_compute_total_cost',store=True)

    def in_process_state(self):
        self.state = 'in_process'

    def completed_state(self):
        self.state = 'completed'
        self.dispatch_date = fields.Date.today()
        self.vehicle_id.status = 'maintenance'
        self.vehicle_id.trip_km = 0

    def generate_bill(self):
        self.state = 'paid'

    def _compute_total_cost(self):
        self.total_cost = 0
        for rec in self.maintenance_lines:
            self.total_cost += rec.cost



class MaintenanceLines(models.Model):
    _name = 'car.rental.maintenance.lines'
    _description = 'Maintenance Lines'
    _rec_name = 'maintenance_id'

    part_id = fields.Many2one('product.product',string='Part ID')
    cost = fields.Float(string='Cost',related='part_id.lst_price')
    maintenance_id = fields.Many2one('car.rental.maintenance',string='Maintenance')