from odoo import models, fields, api


class Patient(models.Model):
    _name = 'hospital.patient'
    _description = 'Patient Model'
    _rec_name = 'patient_name'

    patient_name = fields.Char(string="Patient Name")
    patient_address = fields.Text(string="Patient Address")
    patient_phone = fields.Char(string="Patient Phone Number")
    patient_age = fields.Char(string="Patient Age")
    patient_dob = fields.Date(string="Patient DOB")
    patient_height = fields.Float(string="Patient Height")
    patient_weight = fields.Float(string="Patient Weight")
    disease_description = fields.Text(string='Disease Description')
    health_insurance = fields.Boolean(string="Health Insurance")
    patient_gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender', default='male')
    patient_blood = fields.Selection(
        [('a+', 'A+'), ('b+', 'B+'), ('ab+', 'AB+'), ('o+', 'O+'), ('a-', 'A-'), ('b-', 'B-'), ('ab-', 'AB-'),
         ('o-', 'O-')], string="Patient Blood", default='a+')
    patient_reports = fields.Binary(string="Patient Reports")
    hospital_ids = fields.Many2many('hospital.hospital','hospital_patient_rel','patient_id','hospital_id',string="Patients")
    bill_ids = fields.One2many('account.move','patient_id',string="Bills")