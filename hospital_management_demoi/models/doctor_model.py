from odoo import models,fields,api

class Doctor(models.Model):
    _name = 'hospital.doctor'
    _description = 'Doctor Model'
    _rec_name = 'doctor_name'

    doctor_name = fields.Char(string='Doctor Name')
    doctor_phone = fields.Char(string='Phone Number')
    doctor_dob = fields.Date(string='Date of Birth')
    doctor_gender = fields.Selection([('male','Male'),('female','Female')],string='Gender',default='male')
    joining_date = fields.Date(string="Joining Date")
    doctor_timing = fields.Char(string="Doctor Timing")
    salary = fields.Float(string='Salary')
    doctor_id_proof = fields.Binary(string="Doctor ID Proof")
    doctor_image = fields.Image(string="Doctor Image")
    hospital_id = fields.Many2one('hospital.hospital',string="Hospital",ondelete='cascade')
    appointment_ids = fields.One2many('hospital.appointment',"doctor_id",string="Appointment")
    bill_ids = fields.One2many('account.move','doctor_id',string="Bill")
    department_id = fields.Many2one('hr.department',string="Department",ondelete='cascade')