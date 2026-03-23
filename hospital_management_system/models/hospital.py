from odoo import models,fields,api

class Hospital(models.Model):
    _name = 'hospital.hospital'
    _description = 'Hospital'

    name = fields.Char("Hospital name")
    address = fields.Char("Address")
    contact = fields.Char("Contact number")
    is_active = fields.Boolean("Is active",default=True)
    photo = fields.Image("Image")
    about = fields.Text("About hospital")
    doctor_ids = fields.One2many("hospital.doctor","hospital_id",string="Doctors")

