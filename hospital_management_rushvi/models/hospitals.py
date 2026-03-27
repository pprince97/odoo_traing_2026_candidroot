from odoo import models,fields,api
from odoo.exceptions import ValidationError


class Hospitals(models.Model):
    _name = 'hospital.management.hospitals'
    _description = 'Hospitals'

    name = fields.Char(string='Name',required=True)
    address = fields.Text(string='Address')
    phone = fields.Char(string='Phone',required=True)
    email = fields.Char(string='Email')
    registration_number = fields.Char(string='Registration Number',required=True)
    description = fields.Text(string='Description')
    is_available = fields.Boolean(string='Available',default=True)
    department_ids = fields.Many2many('hospital.management.departments','hospital_department_rel','hospital_id','department_id',string='Departments')
    doctor_ids = fields.Many2many('res.partner','hospital_doctor_rel','hospital_id','doctor_id',string='Doctors',domain="[('department_id','in',department_ids)]")
    patient_ids = fields.One2many('res.partner','hospital_id',string='Patients',domain=[('patient_code','ilike','P%')])
    appointment_ids = fields.One2many('hospital.management.appointments','hospital_id',string='Appointments')
    doc_count = fields.Integer(compute='_compute_count')
    pat_count = fields.Integer(compute='_compute_count')
    app_count = fields.Integer(compute='_compute_count')

    def unlink(self):
        if self.appointment_ids or self.patient_ids or self.doctor_ids:
            raise ValidationError("You cannot delete a hosptial having doctors,patients and appointments.")

    @api.depends('appointment_ids', 'patient_ids', 'doctor_ids')
    def _compute_count(self):
        for rec in self:
            rec.doc_count = len(rec.doctor_ids)
            rec.pat_count = len(rec.patient_ids)
            rec.app_count = len(rec.appointment_ids)

    def view_counts(self):
        if self.env.context.get('patient_ids'):
            return{
                'name': 'Patients',
                'type': 'ir.actions.act_window',
                'res_model': 'res.partner',
                'ref':'view_hospital_management_patients_list',
                'view_mode': 'list,form',
                'domain': [('hospital_id', 'in', self.id)],
                'target': 'current',
            }
        elif self.env.context.get('appointment_ids'):
            return{
                'name': 'Appointments',
                'type': 'ir.actions.act_window',
                'res_model': 'hospital.management.appointments',
                'view_mode': 'list',
                'domain': [('hospital_id', '=', self.id)],
                'target': 'current',
            }
        elif self.env.context.get('doctor_ids'):
            return{
                'name': 'Doctors',
                'type': 'ir.actions.act_window',
                'res_model': 'res.partner',
                'ref':'view_hospital_management_doctors_list',
                'view_mode': 'list',
                'domain': [('hospital_ids', 'in', self.id)],
                'target': 'current',
            }