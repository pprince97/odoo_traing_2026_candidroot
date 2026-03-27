from odoo import models,fields
from datetime import datetime

from pygments.lexer import default


class HmService(models.Model):
    _name = 'hm.service'
    _description = 'Hm Service'

    name = fields.Char('Service Name',required=True)
    type = fields.Selection([('housekeeping','House keeping'),('order','Order'),('laundry','Laundry')],'Service Type' ,default='housekeeping')
    price = fields.Integer('Service Price',default=50)
    quantity = fields.Integer('Service Quantity',default=1)
    is_chargeable = fields.Boolean('Chargeable')
    service_date = fields.Datetime(string='Service Start Datetime',default=fields.Datetime.now)
    description = fields.Text('Service Description')
    attachment = fields.Binary('Service Attachment')
    img = fields.Image('Service Image')
    # service_booking
    booking_ids = fields.Many2many("hm.booking",'booking_service_rel','service_id','booking_id',string="Bookings",ondelete='restrict')
    # service_hotel
    hotel_ids = fields.Many2many("hm.hotel",'hotel_service_rel','service_id','hotel_id',string="Hotels",ondelete='restrict')
