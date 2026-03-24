from odoo import models,fields

class Hotel(models.Model):

    _name='obj.hotel'
    _description='Hotel'

    name=fields.Char("Name")
    t_rooms=fields.Integer("Total rooms")
    rating=fields.Float("Rating (1-10)")
    category=fields.Selection([("luxury","Luxury"),("business","Business"),("budget","Budget")],"Category")
    is_active=fields.Boolean("Is active?")
    o_date=fields.Date("Opening date")
    description=fields.Text("Description")
    lic_doc=fields.Binary("Licence document")
    file_name=fields.Char("File name")
    image=fields.Image("Image")
    file_name_i=fields.Char("Image name")

    room_ids=fields.One2many('obj.room','hotel_id',string="Rooms")
    booking_ids=fields.One2many('obj.booking','hotel_id2',string="Bookings")
    service_ids=fields.Many2many('obj.service','hotel_service_rel','hotel_id','service_id',string="Services")
