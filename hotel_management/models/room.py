from odoo import models, fields


class Room(models.Model):

    _name = 'obj.room'
    _description = 'Room'

    name = fields.Char("Name")
    room_no = fields.Integer("Room Number")
    price_pn = fields.Float("Price per night")
    room_type = fields.Char("Room Type")
    is_available = fields.Boolean("Is available?")
    m_date = fields.Date("Maintenance date")
    last_cleaned = fields.Datetime("Last Cleaned")
    notes = fields.Text("Notes")
    room_doc = fields.Binary("Room document")
    file_name = fields.Char("File namer")
    r_image = fields.Image("Room Images")
    file_name_i = fields.Char("Image namer")

    hotel_id=fields.Many2one("obj.hotel",string="Hotel",ondelete="cascade")
    guest_ids=fields.Many2many('obj.guest','guest_room_rel','room_id','guest_id',string="Guests")

