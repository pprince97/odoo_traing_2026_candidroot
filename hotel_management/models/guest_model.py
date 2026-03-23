from odoo import models,fields

class Guest(models.Model):
    _name ='hotel.guest'
    _description ='Guest Model'
    _rec_name ='guest_name'

    guest_name = fields.Char(string="Guest Name")
    age = fields.Integer(string="Guest's Age")
    discount = fields.Float(string="Guest's Discount")
    gender = fields.Selection([('male','Male'),('female','Female')],string="Guest's Gender")
    is_vip = fields.Boolean(string="Is Vip Guest?")
    date_of_birth = fields.Date(string="Date of Birth")
    check_in_time = fields.Datetime(string="Check In Time")
    remark = fields.Text(string="Guest Remark")
    id_proof = fields.Binary(string="Guest ID Proof")
    guest_photo = fields.Image(string="Guest Photo")

    booking_ids = fields.One2many('hotel.booking','guest_id',string="Booking")
    room_ids = fields.Many2many('hotel.room','guest_room_rel','guest_id','room_id',string="Rooms")