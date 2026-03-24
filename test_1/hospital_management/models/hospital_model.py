# Hospital Name
# ● Address
# ● Phone
# ● Email
# ● Registration Number
# ● Description
# ● Available Departments
# ● Doctors (filtered based on selected department)
# ● Patients
# ● Appointments
# From the Hospital record, we can view all related doctors, patients, and appointments.

from odoo import api, fields, models
from odoo.fields import Domain

class HospitalModel(models.Model):
    _name='hospital.model'
    _description='Hospital'

    name=fields.Char(string='Hospital Name', required=True)
    address=fields.Char(string='Address', required=True)
    phone=fields.Char(string='Phone Number', required=True)
    email=fields.Char(string='Email Address', required=True)
    registration_number=fields.Char(string='Registration Number')
    description=fields.Text(string='Description')

    available_department=fields.Many2many('department.model','hospital_department_relation','hospital_id','department_id',string='Available Department')

    doctor_ids=fields.Many2many('res.partner','hospital_doctor_relation','hospital_id','doctor_id',string='Doctors',domain="[('department_id','in',available_department),('doctor_code','ilike','d%')]",context={'is_doctor':True})
    patient_ids=fields.Many2many('res.partner','hospital_patient_relation','hospital_id','patient_id',string='Patients',domain=[('patient_code','ilike','p%')],context={'is_patient':True})
    appointment_ids=fields.One2many('appointment.model','hospital_id',string='Appointments')

    doctor_count=fields.Integer(string='Doctor Count')
    patient_count=fields.Integer(string='Patient Count')
    appointment_count=fields.Integer(string='Appointment Count')


    def appointment_btn(self):
        self.appointment_count = self.env['appointment.model'].search_count([
            ("hospital_id", "=", self.id),
        ])

        d = {
                'name': "Appointment",
                'type': 'ir.actions.act_window',
                'view_mode': 'list,form',
                'res_model': 'appointment.model',
                'target': 'self',
                'domain': [
                    ("hospital_id", "=", self.id),
                ],
            }

        if self.appointment_count == 1:
            d['view_mode']='form'
            d['res_id']=self.env['appointment.model'].search([("hospital_id", "=", self.id)]).id

        return d

    def doctor_btn(self):
        self.doctor_count = self.env['res.partner'].search_count([
            ("hospital_id", "=", self.id),
            ('doctor_code', 'ilike', 'd%'),
        ])
        d = {
                'name': "Doctor",
                'type': 'ir.actions.act_window',
                'view_mode': 'list,form',
                'res_model': 'res.partner',
                'target': 'self',
                'domain': [
                    ("hospital_id", "=", self.id),
                    ('doctor_code', 'ilike', 'd%'),
                ],
                'context': {'form_view_ref': 'hospital_management.doctor_form'}
            }
        if self.doctor_count == 1:
                d['view_mode'] ='form'
                d['res_id']=self.env['res.partner'].search([
                    ("hospital_id", "=", self.id),
                    ('doctor_code', 'ilike', 'd%'),
                ]).id
        return d

    def patient_btn(self):
        self.patient_count = self.env['res.partner'].search_count([
            ("hospital_ids", "=", self.id),
            ('patient_code', 'ilike', 'p%'),
        ])

        d = {
                'name': "Patient",
                'type': 'ir.actions.act_window',
                'view_mode': 'list,form',
                'res_model': 'res.partner',
                'target': 'self',
                'domain': [
                    ("hospital_ids", "=", self.id),
                    ('patient_code', 'ilike', 'p%'),
                ],
                'context': {'form_view_ref': 'hospital_management.patient_form'},
            }

        if self.patient_count == 1:
               d['view_mode']='form'
               d['res_id'] = self.env['res.partner'].search([
                   ("hospital_ids", "=", self.id),
                   ('patient_code', 'ilike', 'p%'),
               ]).id
        return d

    def create_department(self):

        return{
            'name': 'Department',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'department.wizard',
            'target': 'new',
            'context':{'default_hospital_ids':self.ids}
        }