from odoo import models,fields,api

class Hospital(models.Model):
    _name = 'hospital.hospital'
    _description = 'Hospital Model'
    _rec_name = 'hospital_name'

    hospital_name = fields.Char(string='Hospital Name')
    hospital_address = fields.Text(string='Hospital Address')
    hospital_phone = fields.Char(string='Phone Number')
    hospital_website = fields.Html(string='Website URL')
    is_active = fields.Boolean(default=True)
    doctor_ids = fields.One2many('hospital.doctor','hospital_id',string="Doctors")
    patient_ids = fields.Many2many('hospital.patient','hospital_patient_rel','hospital_id','patient_id',string="Patients")
    department_ids = fields.Many2many('hr.department','hos_dep_rel','hospital_id','department_id',string='Department')
    bill_ids = fields.One2many('account.move','hospital_id',string="Bills")
    appointment_ids = fields.Many2many('hospital.appointment','hos_app_rel','hospital_id','appointment_id',string="Appointments")
