from odoo import models,fields

class Room(models.Model):
    _name = 'hotel.room'
    _description = 'Hotel Room'

    name = fields.Char(string='Room Name')
    room_number = fields.Integer(string='Room Number')
    price_per_night = fields.Float(string='Price Per Night')
    room_type = fields.Char(string='Room Type')
    is_available = fields.Boolean(string='Is Room Available')
    maintenance_date = fields.Date(string="Room's Maintenance Date")
    last_cleaned= fields.Datetime(string="Room's Last Cleaned Date")
    notes = fields.Text(string="Room's Notes")
    room_document = fields.Binary(string="Room's Document")
    room_images = fields.Image(string="Room's Images")

    hotel_ids = fields.Many2many('hotel.hotel','hotel_room_rel','room_id','hotel_id',string="Hotels")
    guest_ids = fields.Many2many('hotel.guest','guest_room_rel','room_id','guest_id',string="Guests")
