from odoo import models, fields,api
from datetime import datetime

class Service(models.Model):

    _name = 'obj.service'
    _description = 'Service'
    _rec_name='s_date'

    name = fields.Char("Service Name")
    s_type = fields.Char("Service Type")
    price = fields.Float("Price")
    quantity = fields.Integer("Quantity")
    is_chargeable = fields.Boolean("Is Chargeable?")
    s_date = fields.Date("Service Date")

    s_time = fields.Datetime("Service time",default=datetime.now())

    description = fields.Text("Description")
    attachment = fields.Binary("Attachment")
    file_name = fields.Char("File names")
    s_image = fields.Image("Service Image")
    file_name_i = fields.Char("Image names")

    booking_ids=fields.Many2many("obj.booking",'booking_service_rel','service_id','booking_id',string="Booking")
    hotel_ids=fields.Many2many('obj.hotel','hotel_service_rel','service_id','hotel_id',string="Hotel")