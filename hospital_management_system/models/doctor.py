from odoo import models,fields,api

class Doctor(models.Model):
    _name = 'hospital.doctor'
    _description = 'Doctor'

    name = fields.Char("Doctor's Name")
    gender = fields.Selection([("male","Male"),("female","Female")],string="Gender")
    dob = fields.Date("Date of birth")
    phone = fields.Char("Phone Number")
    address = fields.Char("Address")
    exp_years = fields.Integer("Experience Years")
    department = fields.Selection([("general_physician","General Physician"),("dentist","Dentist"),("child_specialist","Child Specialist"),
                                  ("cardiologist","Cardiologist"),("dermatologist","Dermatologist"),("psychiatrist","Psychiatrist"),("orthopedic","Orthopedic")],
                                  string="Department")
    status = fields.Selection([("available","Available"),("busy","Busy")],string="Status")
    photo = fields.Image("Photo")
    document = fields.Binary("Degree/Certificate")
    hospital_id = fields.Many2one("hospital.doctor",ondelete="restrict",string="Hospital")
    appointment_ids = fields.One2many("hospital.appointment","doctor_id",string="appointment")
