from odoo import models,fields,api

class Patient(models.Model):
    _name = 'hospital.patient'
    _description = 'Patient'

    app_datetime = fields.Datetime("Application date and time",default=fields.Datetime.now,readonly=True)
    name = fields.Char("Patient Name")
    age = fields.Integer(string="Age")
    gender = fields.Selection([("male","Male"),("female","Female")],string="Gender")
    phone = fields.Char("Phone Number")
    blood_grp = fields.Selection([("A+","A+"),("B+","B+"),("AB+","AB+"),("O+","O+"),("A-","A-"),("B-","B-"),("AB-","AB-"),("O-","O-")],string="Blood group")
    is_handicap = fields.Boolean("Is handicap")
    disease = fields.Char("Disease")
    ward = fields.Selection([("general","General"),("icu","ICU")],string="Ward")
    is_diabetic = fields.Boolean("Is Diabetic")
    have_insurance = fields.Boolean("Have Insurance")
    allergy = fields.Char("Allergy")
    med_history = fields.Binary("Medical history")
    appointment_ids = fields.One2many("hospital.appointment", "patient_id", string="Appointments")
