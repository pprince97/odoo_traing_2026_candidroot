from odoo import models, fields


class Booking(models.Model):

    _name = 'obj.booking'
    _description = 'Booking'

    name = fields.Char("Booking Reference")
    n_nights = fields.Integer("Number Of Nights")
    t_amount = fields.Float("Total amount")
    b_status = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed'),('cancelled','Cancelled')],'Booking Status')
    is_paid = fields.Boolean("Is Paid?")
    b_date = fields.Date("Booking Date")
    ci_dt = fields.Datetime("Check - in date and time")
    s_req = fields.Text("Special Request")
    invoice = fields.Binary("Invoice")
    file_name = fields.Char("File nameb")
    b_image = fields.Image("Booking image proof")
    file_name_i = fields.Char("Image nameb")

    hotel_id2=fields.Many2one("obj.hotel",string="Hotel",ondelete="cascade")
    guest_id=fields.Many2one("obj.guest",string="Guest",ondelete="cascade")
    service_ids=fields.Many2many("obj.service",'booking_service_rel','booking_id','service_id',string="Service")
