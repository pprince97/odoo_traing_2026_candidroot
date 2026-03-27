from odoo import models,fields

class HmHotel(models.Model):
    _name = 'hm.hotel'
    _description = 'Hm Hotel'

    name = fields.Char("Hotel Name",required=True, help="nbffsjkfhsfksdlfdsgs", index=True, copy=True)
    total_rooms = fields.Integer("Total Rooms",required=True)
    rating = fields.Float("Rating")
    category = fields.Selection([('luxury','Luxury'),('business','Business'),('budget','Budget')],"Category",default='budget',required=True)
    is_active = fields.Boolean("Is Active",default=True)
    opening_date = fields.Datetime("Opening Date")
    description = fields.Text("Description")
    license_doc = fields.Binary("License Document",required=True)
    image = fields.Image("Image")
    room_ids = fields.Many2many('hm.room','room_hotel_rel','hotel_id','room_id',string="Rooms",ondelete='restrict')
    booking_ids = fields.One2many('hm.booking','bhotel_id',string="Bookings")
    service_ids = fields.Many2many('hm.service','hotel_service_rel','hotel_id','service_id',string="Services",ondelete='restrict')
    extra_note = fields.Html("Extra Note")
