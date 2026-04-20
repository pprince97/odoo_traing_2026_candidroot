from odoo import api, fields, models

class CarManagement(models.Model):
    _inherit = 'product.product'

    vehicle_code = fields.Char(string='Vehicle Code')
    vehicle_type = fields.Selection([('sedan','Sedan'),('suv','SUV'),('bus','Bus')],string='Vehicle Type')
    currency_id = fields.Many2one(comodel_name='res.currency', string="Foreign Currency")
    cost_per_km = fields.Monetary(store=True, readonly=False,currency_field='currency_id',string='Cost per KM')
    status = fields.Selection([('available','Available'),('booked','Booked'),('maintenance','Maintenance')],string='Status', default='available')
    service_per_km = fields.Float(string='Service per KM')
    per_day_km = fields.Float(string='Per Day KM')
    product_type = fields.Selection([('vehicle','Vehicle',),('parts','Parts')],string='Product Is')
    maintenance_ids = fields.Many2many(comodel_name='rental.maintenance', relation='part_maintenance_rel', column1='part_id', column2='maintenance_id', string='Maintenances')
    maintenance_count = fields.Integer(compute='_compute_maintenance_count')

    @api.model
    def default_get(self, fields_list):
        results = super().default_get(fields_list)
        if 'vehicle_code' in fields_list and not results.get('vehicle_code'):
            results['vehicle_code'] = self.env['ir.sequence'].next_by_code('vehicle.code.seq') or 'New'
        return results

    def _compute_maintenance_count(self):
        self.maintenance_count = self.env['rental.maintenance'].search_count([('vehicle_id', 'in', self.ids)])

    def show_maintenance(self):
        dom = {
            'name': self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'rental.maintenance',
            'view_mode': 'list,form',
            'domain': [('vehicle_id', '=', self.id)],
            'target': 'self'
        }
        if self.maintenance_count == 1:
            dom['view_mode'] = 'form'
            dom['res_id'] = self.env['rental.maintenance'].search([('vehicle_id', '=', self.id)]).id
        return dom


