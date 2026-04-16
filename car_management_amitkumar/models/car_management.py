from odoo import fields, api, models

class CarManagement(models.Model):
    _inherit = 'product.product'
    _description = 'Car Management'

    vehicle_code = fields.Char(string='Vehicle Code')

    vehicle_type = fields.Selection([
        ('sedan', 'Sedan'),
        ('truck', 'Truck'),
        ('suv', 'SUV'),
        ('bus', 'Bus')
    ],
        default='sedan',
        string='Vehicle Type',
    )

    cost_per_km = fields.Float(string='Cost Per KM')
    service_per_km = fields.Float(string='Service Per KM')
    per_day_km = fields.Float(string='Per Day KM')

    status = fields.Selection([
        ('available', 'Available'),
        ('booked', 'Booked'),
        ('maintenance', 'Maintenance'),
    ],
        default='available',
        string='Status',
    )

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            if not val.get('vehicle_code'):
                val['vehicle_code'] = self.env['ir.sequence'].next_by_code('vehicle.code')

        res = super(CarManagement, self).create(vals_list)
        print("\n\nVehicle Code ============> ", res.vehicle_code)
        return res

    def action_available(self):
        self.update({'status': 'available'})

    def action_booked(self):
        self.update({'status': 'booked'})

    def action_maintenance(self):
        self.update({'status': 'maintenance'})


    car_booking_count = fields.Integer(string='Booking Count', compute='get_booking_record')


    def get_booking_record(self):
        self.ensure_one()

        self.car_booking_count = self.env['booking.management'].search_count([('vehicle_detail_ids', '=', self.id)])

        return {
            'type': 'ir.actions.act_window',
            'name': 'Total Booking Record',
            'res_model': 'booking.management',
            'view_mode': 'list,form',
            'domain': [
                ('vehicle_detail_ids', '=', self.id),
            ],
        }