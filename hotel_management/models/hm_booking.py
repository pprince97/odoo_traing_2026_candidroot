from odoo import models,fields

class HmBooking(models.Model):
    _name = "hm.booking"
    _description = "Hm Booking"
    _rec_name = 'booking_ref'
    _inherit =['mail.thread','mail.activity.mixin']

    booking_ref = fields.Char("Booking Ref")
    no_of_nights = fields.Integer("No of Nights",required=True)
    total_amt = fields.Integer("Total Amt")
    booking_status = fields.Selection([('draft', 'Draft'),('confirmed','Confirmed'),('cancelled','Cancelled')],"Booking Status",default='draft',required=True,tracking=True)
    is_paid = fields.Boolean("Is Paid",tracking=True)
    booking_date = fields.Datetime("Booking Date",default=fields.Datetime.now,readonly=True)
    check_in_dt = fields.Datetime("Check in Date")
    special_req = fields.Text("Special Req")
    invoice = fields.Binary("Invoice")
    booking_img_proof = fields.Image("Booking Image Proof")
    # booking_hotel
    bhotel_id = fields.Many2one("hm.hotel","Hotel",ondelete="cascade")
    # guest_booking
    guest_id = fields.Many2one("hm.guest",string="Guest",ondelete="cascade")
    # booking_service
    service_ids = fields.Many2many("hm.service","booking_service_rel","booking_id","service_id",string="Services")

    # @api.depends('booking_status', 'is_paid')
    # def _compute_full_display_name(self):
    #     for record in self:
            # status_label = dict(record._fields['booking_status'].selection).get(record.booking_status, '')
            # record.full_display_name = f"{status_label} | Paid: {record.is_paid}"