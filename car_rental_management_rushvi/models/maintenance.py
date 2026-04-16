from odoo import api, fields, models, tools

class Maintenance(models.Model):
    _name = 'car.rent.maintenance'
    _description = 'Maintenance'
    _rec_name = 'vehicle_id'

    vehicle_id = fields.Many2one('product.product',string='Vehicle', domain=[('vehicle_code','!=',False)])
    current_kms = fields.Float(string='Current Kms')
    arrival_date = fields.Date(string='Arrival Date')
    dispatch_date = fields.Date(string='Dispatch Date')
    parts_added_ids = fields.One2many('product.product','maintenance_id',string='Parts Add')
    service_cost = fields.Float(string='Service Cost')
    parts_cost = fields.Float(string='Parts Cost',default=0,store=True)
    total_cost = fields.Float(string='Total Cost',compute='_compute_total_cost',store=True)

    @api.onchange('parts_added_ids')
    def onchange_parts_added_ids(self):
        self.parts_cost = sum(self.parts_added_ids.mapped('lst_price'))

    @api.depends('parts_added_ids','service_cost')
    def _compute_total_cost(self):
        self.total_cost = self.service_cost + self.parts_cost