from odoo import models,fields
from datetime import datetime

class Service(models.Model):
    _name = 'hotel.service'
    _description = 'Service Model'
    _rec_name = 'service_name'

    service_name = fields.Char(string="Service Name")
    service_type = fields.Char(string="Service Type")
    price = fields.Float(string="Service Price")
    quantity = fields.Integer(string="Quantity")
    is_chargeable = fields.Boolean(string="Is Service Chargeable")
    service_date = fields.Date(string="Service Date")
    service_time = fields.Datetime(string="Service Time",default=datetime.now())
    description = fields.Text(string="Service Description")
    attachment = fields.Binary(string="Attachment")
    service_image = fields.Image(string="Service Image")

    booking_ids = fields.Many2many('hotel.booking','booking_service_rel','service_id','booking_id',string='Bookings')
    hotel_ids = fields.Many2many('hotel.hotel','hotel_service_rel','service_id','hotel_id',string='Hotels')
