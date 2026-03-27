from odoo import models,fields

class HmGuest(models.Model):
    _name = "hm.guest"
    _description = "Hm Guest"

    name=fields.Char("Guest Name",required=True)
    age= fields.Integer("Age")
    discount=fields.Float("Discount",default=0,required=True)
    gender=fields.Selection([("male","Male"),("female","Female")],"Gender",default="female")
    is_vip= fields.Boolean("is VIP",default=True)
    dob = fields.Date("Date of Birth")
    check_in_time = fields.Datetime("Check In Time")
    remarks = fields.Text("Remarks")
    id_proof=fields.Binary("ID Proof",required=True)
    guest_photo =  fields.Image("Guest Photo")
    room_id = fields.Many2one('hm.room',string='Room', domain=[('room_type','=','suite')])
    booking_ids = fields.One2many('hm.booking','guest_id',string='Bookings')
# class_id = fields.Many2one('school_management_system.student_class',string='Class', ondelete='cascade')