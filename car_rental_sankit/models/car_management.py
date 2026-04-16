from odoo import api, fields, models


class CarManagement(models.Model):
    _inherit = 'product.product'
    # name  is already in product.product
    is_what = fields.Selection([
        ('car', 'Car'),
        ('part', 'Part'),
        ('product', 'Product'),
    ])
    vehicle_code = fields.Char(string="Vehicle Code")
    vehicle_type = fields.Selection([
        ('sedan', 'Sedan'),
        ('suv', 'SUV'),
        ('bus', 'Bus')
    ])
    cost_per_km = fields.Float(string="Cost per Km")
    status = fields.Selection([
        ('available', 'Available'),
        ('booked', 'Booked'),
        ('maintenance', 'Maintenance'),
    ],
        default='available',
        string="Status",
    )
    service_per_km = fields.Float(string="Service per Km")
    min_km_per_day = fields.Float(string="Min Km per Day")

    # Smart Button
    maintenance_ids = fields.One2many('car.maintenance','vehicle_id',string="Maintenances")

    # Sequence
    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            if not val.get('vehicle_code'):
                val['vehicle_code'] = self.env['ir.sequence'].next_by_code('rental.sequence')
        res = super().create(vals_list)
        return res

    def maintenance_history(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Maintenance',
            'view_mode': 'list,form',
            'res_model': 'car.maintenance',
            'domain': [('vehicle_id', '=', self.id)],
        }


