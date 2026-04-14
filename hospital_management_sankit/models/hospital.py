from odoo import fields , models , api

class Hospital(models.Model):
    _name = 'hospital.hospital'
    _description = 'Hospital'
    _rec_name = 'hospital_name'

    hospital_name = fields.Char(string="Name",required=True)
    address = fields.Char(string="Address")
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    registration_number = fields.Char(string="Registration Number")
    description = fields.Text(string="Description")


    department_ids = fields.Many2many('hospital.department', 'hospital_department_rel' ,'hospital_id','department_id',string="Departments")
    doctor_ids = fields.One2many('res.partner','hospital_id', string="Doctors" , domain="([('doctor_code', 'ilike', 'D/%')])")
    patient_ids = fields.One2many('res.partner','p_hospital_id',string="Patients" , domain="([('patient_code', 'ilike', 'P/%')])")
    appointment_ids = fields.One2many('hospital.appointment', 'hospital_id', string="Appointments")
