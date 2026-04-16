from odoo import fields, api, models

class DriverManagement(models.Model):
    _inherit = 'res.partner'
    _description = 'Driver Management'

    license_details = fields.Char("License Details (No)")
    driver_per_day_rate = fields.Float("Driver per Day Rate")

    member = fields.Selection([('driver', 'Driver'),('other', 'Other')])

    status = fields.Selection([
        ('available', 'Available'),
        ('unavailable', 'Unavailable')
    ],
        default='available',
    )

    driver_booking_count = fields.Integer(string='Booking Count', compute='get_booking_record')

    def get_booking_record(self):
        self.ensure_one()

        self.driver_booking_count = self.env['booking.management'].search_count([('customer_detail_ids', '=', self.id)])

        return {
            'type': 'ir.actions.act_window',
            'name': 'Total Booking Record',
            'res_model': 'booking.management',
            'view_mode': 'list,form',
            'domain': [
                ('customer_detail_ids', '=', self.id),
            ],
        }