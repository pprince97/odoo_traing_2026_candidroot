from odoo import api, fields, models

class ProductVehicle(models.Model):
    _inherit = "product.product"

    is_part = fields.Boolean(string="Is Part")
    is_vehicle = fields.Boolean(string="Vehicle")
    vehicle_code = fields.Char(string="Vehicle Code",readonly=True)
    vehicle_type = fields.Selection([('sedan','Sedan'),('suv','SUV'),('bus','Bus')],string="Vehicle Type",required=True)
    cost_per_km = fields.Float(string="Cost per KM",required=True)
    status = fields.Selection([('available','Available'),('booked','Booked'),('maintenance','Maintenance')],string="Status",default='available')
    service_per_km = fields.Float(string="Service per KM",required=True)
    per_day_km = fields.Float(string="Per-Day KM",required=True)
    maintenance_ids = fields.One2many('vehicle.maintenance','vehicle_id',string="Maintenance")
    maintenance_records_count = fields.Integer(string="Maintenance Record Count")
    booking_line_ids = fields.One2many('vehicle.booking.line','vehicle_id',string="Booking Line")


    def maintenance_records(self):
        records = self.env['vehicle.maintenance']
        self.maintenance_records_count = records.search_count([
            ("vehicle_id", "=", self.id),
        ])
        return {
            'name': "Maintenance Records",
            'type': 'ir.actions.act_window',
            'view_mode': 'list,form',
            'res_model': 'vehicle.maintenance',
            'target': 'self',
            'domain': [
                ("vehicle_id", "=", self.id),
            ],
        }

    @api.model_create_multi
    def create(self, vals):
        for rec in vals:
            rec['vehicle_code'] = self.env['ir.sequence'].next_by_code('vehicle.seq') or 'New'
        res = super(ProductVehicle, self).create(vals)
        return res