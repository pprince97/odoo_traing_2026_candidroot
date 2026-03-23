from odoo import models,fields,api

class RoomModel(models.Model):
    _name = 'hotel.room'
    _description = 'Room'

    name=fields.Char(string="Room Name")
    room_no=fields.Integer(string="Room Number")
    price_per_night=fields.Float(string="Price per Night")
    room_type=fields.Char(string="Room Type")
    is_available=fields.Boolean(string="Is Available?")
    maintenance_date=fields.Date(string="Maintenance Date")
    last_cleaned=fields.Datetime(string="Last Cleaned")
    notes=fields.Text(string="Notes")
    room_document=fields.Binary(string="Room Document")
    room_images=fields.Image(string="Room Images")

    hotel_ids=fields.Many2many('hotel.hotel','room_hotel_rel','room_id','hotel_id',string='Hotels')
    guest_ids=fields.Many2many('hotel.guest','guest_room_rel','room_id','guest_id',string='Guestss')

