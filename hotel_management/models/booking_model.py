from odoo import models,fields,api


class BookingModel(models.Model):
    _name = 'hotel.booking'
    _description = 'Booking'
    _rec_name='booking_reference'
    _inherit=['mail.thread','mail.activity.mixin']

    booking_reference=fields.Char(string='Booking Reference')
    no_of_nights=fields.Integer(string='No of Nights',required=True,default=0)
    total_amount=fields.Float(string='Total amount',required=True)
    booking_status=fields.Selection([('draft','Draft'),('confirmed','Confirmed'),('cancelled','Cancelled')],'Booking Status',tracking=True)
    is_paid=fields.Boolean(string='Is Paid?',default=True)
    booking_date=fields.Date(string='Booking Date',tracking=True,default=fields.Date.today(),readonly=True)
    check_in_datetime=fields.Datetime(string='Check in Date and Time',tracking=True)
    special_request=fields.Text(string='Special Request')
    invoice=fields.Binary(string='Invoice')
    booking_image_proof=fields.Image(string='Booking Image Proof',required=True)

    hotel_id=fields.Many2one('hotel.hotel',string='Hotel',ondelete='restrict')
    guest_id=fields.Many2one('hotel.guest',string='Guest',ondelete='restrict')
    service_ids=fields.Many2many('hotel.service','service_booking_rel','booking_id','service_id',string='Services')

