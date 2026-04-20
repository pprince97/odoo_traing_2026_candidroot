from odoo import models, fields, api

class Driver(models.Model):
    _inherit = 'res.partner'

    # name
    licence_no = fields.Char(string='Licence Number',required=True)
    licence_prof = fields.Binary(string='Licence Profile',required=True,attachment=True)
    # phone
    status = fields.Selection([('available', 'Available'),('not_available', 'Not Available')],default='available',string='Driver Status')
    per_day_rate = fields.Float(string='Rate per day',required=True)
    is_driver = fields.Boolean(string='Driver')
    booking_count = fields.Integer(string='Booking Count',compute='_compute_booking_count')

    def _compute_booking_count(self):
        self.booking_count = self.env['car.rental.booking'].search_count([('driver_id','=',self.id)])


    def booking_records(self):
        self.booking_count = self.env['car.rental.booking'].search_count([('driver_id','=',self.id)])
        rp = {
            'type': 'ir.actions.act_window',
            'res_model': 'car.rental.booking',
            'view_mode': 'list,form',
            'domain': [('driver_id','=',self.id)],
            'target': self
        }
        if self.booking_count == 1:
            rp['view_mode'] = 'form'
            rp['res_id'] = self.env['car.rental.booking'].search(
                [('driver_id','=',self.id)]).id
        return rp