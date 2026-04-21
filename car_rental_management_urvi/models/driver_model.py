from odoo import models, fields, api

class Driver(models.Model):
    _inherit = 'res.partner'

    # name
    licence_no = fields.Char(string='Licence Number')
    licence_prof = fields.Binary(string='Licence Profile',attachment=True)
    # phone
    status = fields.Selection([('available', 'Available'),('not_available', 'Not Available')],default='available',string='Driver Status',readonly=True)
    per_day_rate = fields.Float(string='Rate per day')
    is_driver = fields.Boolean(string='Driver')
    booking_count = fields.Integer(string='Booking Count',compute='_compute_booking_count')

    def _compute_booking_count(self):
        self.booking_count = self.env['car.rental.booking'].search_count([('booking_lines.driver_id','=',self.id)])


    def booking_records(self):
        self.booking_count = self.env['car.rental.booking'].search_count([('booking_lines.driver_id','=',self.id)])
        rp = {
            'type': 'ir.actions.act_window',
            'res_model': 'car.rental.booking',
            'view_mode': 'list,form',
            'domain': [('booking_lines.driver_id','=',self.id)],
            'target': self
        }
        if self.booking_count == 1:
            rp['view_mode'] = 'form'
            rp['res_id'] = self.env['car.rental.booking'].search(
                [('booking_lines.driver_id','=',self.id)]).id
        return rp