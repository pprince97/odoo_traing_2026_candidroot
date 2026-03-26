from odoo import models, fields


class Guest(models.Model):

    _name = 'obj.guest'
    _description = 'Guest'

    name = fields.Char("Name")
    age = fields.Integer("Age")
    discount = fields.Integer("Discount")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')],'Gender')
    is_vip = fields.Boolean("Is VIP?")
    dob = fields.Date("Date Of Birth")
    ci_time = fields.Datetime("Check - in Time")
    remark = fields.Text("Remarks")
    id_proof = fields.Binary("Id Proof")
    file_name = fields.Char("File nameg")
    g_image = fields.Image("Guest Photo")
    file_name_i = fields.Char("Image nameg")

    booking_ids=fields.One2many('obj.booking','guest_id',string="Bookings")
    room_ids=fields.Many2many('obj.room','guest_room_rel','guest_id','room_id',string="Rooms")