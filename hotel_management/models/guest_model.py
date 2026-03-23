from odoo import models,fields,api

class GuestModel(models.Model):
    _name = 'hotel.guest'
    _description = 'Guest'
    _rec_name='guest_name'

    guest_name=fields.Char(string='Guest Name')
    age=fields.Char(string='Age')
    discount=fields.Float(string='Discount')
    gender=fields.Selection([('male','Male'),('female','Female')],string='Gender')
    is_vip=fields.Boolean(string='Is VIP?')
    dob=fields.Date(string='Date of Birth')
    check_in_time=fields.Datetime(string='Check in Time')
    remark=fields.Text(string='Remark')
    id_proof=fields.Binary(string='ID Proof')
    guest_photo=fields.Image(string='Guest Photo')

    booking_ids=fields.One2many('hotel.booking','guest_id',string='Bookings')
    room_ids=fields.Many2many('hotel.room','guest_room_rel','guest_id','room_id',string='Rooms')
