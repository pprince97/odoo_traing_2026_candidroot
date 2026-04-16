from odoo import api, fields, models


class Driver(models.Model):
    _inherit = 'res.partner'
    # name ,address , phone is already in res.partner

    is_what = fields.Selection([
        ('driver', 'Driver'),
        ('partner', 'Partner'),
    ])
    pan_number = fields.Char(string="Pan Number")
    license_number = fields.Char(string="Licence Number")
    address = fields.Char(string="Address")

    status = fields.Selection([
        ('available', 'Available'),
        ('booked', 'Booked'),
    ],
        default='available',
        string="Status",
    )

    per_day_rate = fields.Float(string="Rate per day")

    booking_record_ids = fields.One2many('record.booking','driver_id',string="Record Bookings")

    def booking_record_history(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Booking Record',
            'view_mode': 'list,form',
            'res_model': 'record.booking',
            'domain': [('driver_id', '=', self.id)],
        }