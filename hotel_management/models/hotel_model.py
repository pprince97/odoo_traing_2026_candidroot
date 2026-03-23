from odoo import models,fields,api

class HotelModel(models.Model):
    _name = 'hotel.hotel'
    _description = 'Hotel'

    name=fields.Char(string='Name')
    total_rooms=fields.Integer(string='Total Rooms')
    rating=fields.Float(string='Rating')
    category=fields.Selection([('luxury','Luxury'),('business,','Business'),('budget','Budget')],
                         'Category')
    is_active=fields.Boolean(string="Is Active",default=True)
    opening_date=fields.Date(string="Opening Date")
    description=fields.Text(string="Description")
    license=fields.Binary(string="License")
    image=fields.Image(string="Image")

    room_ids=fields.Many2many('hotel.room','room_hotel_rel','hotel_id','room_id',string='Rooms')
    booking_ids=fields.One2many('hotel.booking','hotel_id',string='Bookings')
    service_ids=fields.Many2many('hotel.service','hotel_service_rel','hotel_id','service_id',string='Services')
