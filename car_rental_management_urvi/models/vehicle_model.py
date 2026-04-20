from odoo import api, fields, models

class Vehicle(models.Model):
    _inherit = 'product.product'

    vehicle_type = fields.Selection([('sedan','Sedan'),('suv','SUV'),('bus','Bus')],string='Vehicle Type',default='sedan',required=True)
    status = fields.Selection([('available','Available'),('booked','Booked'),('maintenance','Maintenance')],string='Vehicle Status',default='available')
    service_per_km = fields.Integer(string='Service Per-KM',required=True)
    per_day_km = fields.Integer(string='Per-Day KM',required=True)
    trip_km = fields.Integer(string='Trip KM')
    required_maintenance = fields.Boolean(string='Required Maintenance',compute='_compute_maintenance')
    main_count = fields.Integer(string='Main Count',compute='_compute_main_count')

    @api.model
    def default_get(self, fields):
        defaults = super(Vehicle, self).default_get(fields)
        if self.env.context.get('vehicles'):
            defaults['type'] = 'vehicle'
            if defaults.get('default_code', 'New') == 'New':
                defaults['default_code'] = self.env['ir.sequence'].next_by_code('vehicle.sequence') or 'New'
        return defaults

    @api.depends('trip_km','service_per_km')
    def _compute_maintenance(self):
        for record in self:
            if record.trip_km >= record.service_per_km:
                record.required_maintenance = True
            else:
                record.required_maintenance = False

    def _compute_main_count(self):
        self.main_count = self.env['car.rental.maintenance'].search_count([('vehicle_id','=',self.id)])

    def maintenance_records(self):
        self.main_count = self.env['car.rental.maintenance'].search_count([('vehicle_id', '=', self.id)])
        rp = {
            'type': 'ir.actions.act_window',
            'res_model': 'car.rental.maintenance',
            'view_mode': 'list,form',
            'domain': [('vehicle_id','=',self.id)],
            'target': self
        }
        if self.main_count == 1:
            rp['view_mode'] = 'form'
            rp['res_id'] = self.env['car.rental.maintenance'].search(
                [('vehicle_id','=',self.id)]).id
        return rp


class ProductVarient(models.Model):
    _inherit = 'product.template'

    type = fields.Selection(selection_add=[('vehicle','Vehicle')],ondelete={
            'vehicle': 'cascade'
        })