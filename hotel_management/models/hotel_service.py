from odoo import models, fields, api

class HotelService(models.Model):
    _name = 'hotel.service'
    _description = 'Hotel Service'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'service_name'

    service_name = fields.Char(string='Service Name')
    service_type = fields.Selection([('cleaning', 'Cleaning'),
                                     ('maintenance', 'Maintenance'),
                                     ('spa','Spa'),
                                     ('gym','Gym'),
                                     ('parking','Parking'),] , tracking=True)
    price = fields.Float(string='Price' , tracking=True , digits=(16,1))
    # price = fields.Monetary(string='Price' , tracking=True )
    Quantity = fields.Float(string='Quantity' , tracking=True)
    is_chargeable = fields.Boolean(string='Is Chargeable' , tracking=True)
    service_date = fields.Date(string='Service Date')
    service_time = fields.Datetime(string='Service Time',default=fields.Datetime.now)
    description = fields.Text(string='Description')
    attachment = fields.Binary(string='Attachment')
    service_image = fields.Binary(string='Service Image')

    booking_ids = fields.Many2many('hotel.booking','booking_service_rel','service_id','booking_id', string='Booking Ids')
    hotel_id = fields.Many2one('hotel.hotel', string='Hotel Id')


    # booking_count = fields.Integer(string='Booking Count',default=0 , compute='compute_booking_count')


    def action_hotel_service(self):
        self.ensure_one()

        booking = self.env['hotel.booking'].search([('service_ids', '=', self.id)])

        if len(booking) == 1 or len(booking) == 0:
            return {
                'name': "Bookings",
                'type': 'ir.actions.act_window',
                'res_model': 'hotel.booking',
                'domain': [('service_ids', '=', self.id)],
                'view_mode': 'form',
                'res_id': booking.id,

                # 'views': [(self.env.ref('hotel.booking').id, 'form')],
            }
        else:
            return {
                'name': "Bookings",
                'type': 'ir.actions.act_window',
                'res_model': 'hotel.booking',
                'view_mode': 'list,form',
                'domain': [('service_ids', '=', self.id)],
            }
