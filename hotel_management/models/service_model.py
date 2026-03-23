from odoo import models,fields,api

class ServiceModel(models.Model):
    _name='hotel.service'
    _description='Service'
    _rec_name='service_name'

    service_name=fields.Char(string='Service Name')
    service_type=fields.Char(string='Service Type')
    price=fields.Float(string='Price')
    quantity=fields.Integer(string='Quantity')
    is_chargeable=fields.Boolean(string='Is Chargeable?')
    service_date=fields.Date(string='Service Date')
    service_time=fields.Datetime(string='Service Time',default=fields.Datetime.now)
    description=fields.Text(string='Description')
    attachment=fields.Binary(string='Attachment')
    service_image=fields.Image(string='Service Image')

    booking_ids=fields.Many2many('hotel.booking','service_booking_rel','service_id','booking_id',string='Bookings')
    hotel_ids = fields.Many2many('hotel.hotel', 'hotel_service_rel', 'service_id', 'hotel_id', string='Hotels')
