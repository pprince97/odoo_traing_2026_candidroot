from odoo import api, models, fields, exceptions
from odoo.exceptions import ValidationError


class Drivers(models.Model):
    _inherit = 'res.partner'

    license_number = fields.Char('License Number')
    license_issue_date = fields.Date('License Issue date')
    license_expire_date = fields.Date('License Expire Date')
    status = fields.Selection([('available', 'Available'), ('on_trip', 'On Trip')], default='available')
    driver_per_day_rate = fields.Float("Driver's Rate per Day")
    age = fields.Integer("Age")
    driver_code = fields.Char("Driver Code")
    booking_count = fields.Integer("Booking Count", compute='_compute_booking_count')

    def status_available(self):
        self.status = 'available'

    def status_on_trip(self):
        self.status = 'on_trip'

    @api.model_create_multi
    def create(self, vals_list):
        res = super(Drivers, self).create(vals_list)
        if self.env.context.get('driver'):
            for rec in res:
                if not rec.driver_code:
                    rec.driver_code = self.env['ir.sequence'].next_by_code('driver.seq') or 'New'
                    group_driver = self.env.ref('base.group_portal')
                    user_id = self.env['res.users'].create({'name': rec.name, 'login': rec.name, 'password': rec.name,
                                                            'group_ids': [(4, group_driver.id)],
                                                            'partner_id': rec.id})
                    rec.user_id = user_id
        else:
            for rec in res:
                group_customer = self.env.ref('base.group_portal')
                user_id = self.env['res.users'].create({'name': rec.name, 'login': rec.name, 'password': rec.name,
                                                        'group_ids': [(4, group_customer.id)],
                                                        'partner_id': rec.id})
                rec.user_id = user_id
        return res


    @api.onchange('license_issue_date','license_expire_date')
    def onchange_license_dates(self):
        if self.license_issue_date and self.license_expire_date and self.license_issue_date > self.license_expire_date:
            raise ValidationError("Issue Date cannot be after expire Date")

    def view_bookings(self):
        return {
            'name': 'Bookingst',
            'type': 'ir.actions.act_window',
            'res_model': 'car.rent.booking',
            'view_mode': 'list,form',
            'domain': [('booking_vehicle_ids.driver_id', 'in', self.id)],
            'target': 'current',
        }

    def _compute_booking_count(self):
        self.booking_count = self.env['car.rent.booking'].search_count([('booking_vehicle_ids.driver_id.id', '=', self.id)])

        #