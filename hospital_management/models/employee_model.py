from odoo import models, fields, api
import random


class Employee(models.Model):
    _inherit = "hr.employee"

    is_medical_staff = fields.Boolean(string="Medical Staff")
    License_no = fields.Char(string="License_no")
    specialization = fields.Selection([('cardio', 'Cardio'), ('neuro', 'Neuro'), ('general', 'General')],string="Specialization", default='cardio')
    consultation_fee = fields.Float(string="Consultation_fee")
    experience_years = fields.Integer(string="Experience_years")
    joining_datetime = fields.Datetime(string="Joining_datetime")
    patient_ids = fields.One2many('hospital.patient', 'doctor_employee_id', string="Patients")
    signature_image = fields.Char(string="Signature")
    notes_html = fields.Html(string="Notes_html")
    patient_count = fields.Integer(string="Patient_count")
    doctor_count = fields.Integer(string="Doctor_counts")

    def approve_doctor(self):
        self.doctor_count = self.env['hospital.doctor'].with_context(
            {'available':True}).search_count([('max_patients','>',5)])
        return {
            'name': self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'hospital.doctor',
            'view_mode': 'list',
            'domain': [('max_patients','>',5)],
            'target': self
        }

    def patient_list(self):
        self.patient_count = self.env['hospital.patient'].search_count(
            [('reference_field', '=', 'employee'), ('doctor_employee_id', '=', self.id)])
        return {
            'name': self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'hospital.patient',
            'view_mode': 'list,form',
            'domain': [('reference_field', '=', 'employee'), ('doctor_employee_id', '=', self.id)],
            'target': self
        }
