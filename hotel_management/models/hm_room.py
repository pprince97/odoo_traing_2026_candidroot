from odoo import models,fields

class HmRoom(models.Model):
    _name = 'hm.room'
    _description = 'HM Room'

    name = fields.Char("Room Name")
    number = fields.Char("Room Number")
    price_per_night = fields.Integer("Price per Night",required=True,default=1000)
    room_type=fields.Selection([('suite','Suite'),('deluxe','Deluxe'),('standard','Standard')],'Room Type',default='standard')
    is_available = fields.Boolean("Available",default=True)
    maintenance = fields.Date("Maintenance Date")
    last_cleaned = fields.Datetime("Last Cleaned Date")
    notes = fields.Text("Notes")
    room_document = fields.Binary("Room Document",required=True)
    room_image = fields.Image("Room Image")
    guest_ids = fields.One2many('hm.guest','room_id',string="Guests")
    hotel_ids = fields.Many2many('hm.hotel','room_hotel_rel','room_id','hotel_id',string="Hotels")

    # subject_ids = fields.Many2many('school_management_system.subject','student_subject_rel','student_id','subject_id',string='Subjects')

