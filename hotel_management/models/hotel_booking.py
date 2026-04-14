from odoo import models, fields, api, Command


class HotelBooking(models.Model):
    _name = 'hotel.booking'
    _description = 'Hotel Booking'

    booking_reference = fields.Char(string='Booking Reference')
    number_of_nights = fields.Integer(string='Number of Nights', )
    total_amount = fields.Float(string='Total Amount')
    booking_status = fields.Selection([('draft','Draft'),
                                       ('confirmed','Confirmed'),
                                       ('cancelled','Cancelled'),])
    is_paid = fields.Boolean(string='Is Paid?')
    booking_date = fields.Date(string='Booking Date')
    check_in_date_and_time = fields.Datetime(string='Check In Date and Time')
    special_request= fields.Text(string='Special Request')
    invoice= fields.Binary(string='Invoice')
    booking_image_proof = fields.Image(string='Booking Image Proof')

    hotels_ids = fields.Many2many('hotel.hotel','hotel_booking_rel','booking_id','hotel_id' ,string='Hotels Ids')
    guest_id = fields.Many2one('hotel.guest', string = 'Guest Id')
    service_ids = fields.Many2many('hotel.service','booking_service_rel','booking_id','service_id' ,string='Service Ids')




    def create_booking_with_service(self):
        booking = self.env['hotel.booking'].create({
            'booking_reference': 'san123',
            'number_of_nights': '2',
            'service_ids': [
                Command.create({
                    'service_name': 'Thai',
                    'service_type': 'spa',
                })
            ]
        })

    def update_booking_with_service(self):
        print("_____11____",self.env.context)
        booking = self.write({
            'service_ids': [
                Command.update(3,{
                    'service_name': 'sanjay',
                    'service_type': 'cleaning',
                })
            ]
        })

    # def unlink_booking_with_service(self):
    #     booking = self.write({
    #         'service_ids': [
    #             Command.unlink(3)
    #         ]
    #     })
    def link_booking_with_service(self):
        booking = self.write({
            'service_ids': [
                Command.link(3)
            ]
        })

    # def set_booking_with_service(self):
    #     booking = self.write({
    #         'service_ids': [
    #             Command.set([3])
    #         ]
    #     })

    def set_booking_with_service(self):
        if self.env.context.get('from_booking'):
            print("Called from booking form")

    def action_server_is_paid(self):
        for rec in self:
            records = self.env['hotel.booking'].search([('id','=',rec.id)])
            records.write({'is_paid':True})




