from odoo import models, fields, api

class Hotel(models.Model):
    _name = 'hotel.hotel'
    _description = 'List of the hotel'

    name = fields.Char(string='Name', required=True)
    total_rooms = fields.Integer(string='Total rooms', required=True)
    rating = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    ],string='Rating')
    category = fields.Selection([('luxury','Luxury'),('business','Business'),('budget','Budget'),],string='Category')
    is_active = fields.Boolean(string='Is Active')
    opening_date = fields.Date(string='Opening Date')
    description = fields.Text(string='Description')
    license_document = fields.Binary(string='License Document')
    image = fields.Image(string='Image')

    room_ids = fields.One2many('hotel.room', 'hotel_id', string='Rooms Ids')
    booking_ids = fields.Many2many('hotel.booking','hotel_booking_rel','hotel_id','booking_id',string='Bookings Ids')
    service_ids = fields.One2many('hotel.service','hotel_id',string='Service Ids')


