from odoo import models,fields
from datetime import datetime

class Booking(models.Model):
    _name = 'hotel.booking'
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = 'Booking Model'
    _rec_name = 'booking_reference'

    booking_reference = fields.Char(string='Booking Reference',tracking=True,required=True)
    number_of_nights = fields.Integer(string='Number of Nights')
    total_amount = fields.Float(string='Total Amount',default=0)
    booking_status = fields.Selection([('draft','Draft'),('confirmed','Confirmed'),('cancelled','Cancelled')],string='Booking Status',default='draft')
    is_paid = fields.Boolean(string='Is Paid Booking?')
    booking_date = fields.Date(string='Booking Date & Time',tracking=True)
    checkin_date = fields.Datetime(string='Checkin Date Time',default=datetime.now(),readonly=True)
    special_request = fields.Text(string='Special Request')
    invoice = fields.Binary(string='Invoice')
    booking_image_proof = fields.Image(string='Booking Image Proof')

    hotel_id = fields.Many2one('hotel.hotel',string='Hotel',ondelete='restrict')
    guest_id = fields.Many2one('hotel.guest',string='Guest',ondelete='cascade')
    service_ids = fields.Many2many('hotel.service','booking_service_rel','booking_id','service_id',string='Service')
