from odoo import models, fields, api , Command



class HotelGuest(models.Model):
    _name = 'hotel.guest'
    _description = 'Hotel guest'
    _rec_name = 'guest_name'

    guest_name = fields.Char(string='Guest Name')
    age = fields.Integer(string='Age')
    discount = fields.Float(string='Discount')
    gender = fields.Selection([('male', 'Male'),
                               ('female', 'Female')],)
    is_vip=fields.Boolean(string='Is Vip?')
    date_of_birth = fields.Date(string='Date of Birth')
    check_in_time = fields.Datetime(string='Check In Time')
    remark = fields.Text(string='Remark')
    id_proof = fields.Binary(string='ID Proof')
    guest_photo = fields.Image(string='Guest Photo')

    booking_ids = fields.One2many('hotel.booking','guest_id',string='Bookings Ids')
    room_id = fields.Many2one('hotel.room',string='Room Id')

    def create_guest_with_booking(self):
        booking = self.env['hotel.guest'].create({
            'guest_name': 'sunil',
            'age': '2',
            'booking_ids': [
                # Command.create({
                #     'booking_reference': 'sun123',
                #     'number_of_nights': 12,
                # })
                Command.update(2,{
                    'booking_reference': 'ram456',
                        'number_of_nights': 456,
                })
            ]
        })

    def update_guest_with_booking(self):
        booking = self.write({
            'booking_ids': [
                # Command.create({
                #     'booking_reference': 'sun123',
                #     'number_of_nights': 12,
                # })
                Command.update(6,{
                    'booking_reference': 'ajay1',
                        'number_of_nights': 123,
                })
            ]
        })

    def delete_guest_with_booking(self):
        booking = self.write({
            'booking_ids': [
                Command.delete(5),
            ]
        })

    def link_guest_with_booking(self):
        booking = self.write({
            'booking_ids': [
                Command.link(6)
            ]
        })
    def clear_guest_with_booking(self):
        print("_____22____", self.env.context)
        booking = self.write({
            'booking_ids': [
                Command.clear()
            ]
        })