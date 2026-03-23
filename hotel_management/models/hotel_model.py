from odoo import models,fields

class Hotel(models.Model):
    _name ='hotel.hotel'
    _description ='Hotel Model'

    name = fields.Char(string='Hotel Name')
    total_rooms = fields.Integer(string='Total Hotel Rooms')
    rating = fields.Float(string='Hotel Rating')
    category = fields.Selection([('luxury','Luxury'),('business','Business'),('budget','Budget')],string='Hotel Category')
    is_active = fields.Boolean(string='Is Hotel Active')
    opening_date = fields.Date(string='Hotel Opening Date')
    description = fields.Text(string='Hotel Description')
    license_document = fields.Binary(string="Hotel's Licensed Document")
    image = fields.Image(string="Hotel Image")
    # hotel_m = fields.Monetary(string="Hotel Monetary")

    room_ids = fields.Many2many('hotel.room','hotel_room_rel','hotel_id','room_id',string="Rooms")
    booking_ids = fields.One2many('hotel.booking','hotel_id',string='Booking IDs')
    service_ids = fields.Many2many('hotel.service','hotel_service_rel','hotel_id','service_id',string="Services")