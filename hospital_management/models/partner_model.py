from odoo import models, fields, api
import random

class Partner(models.Model):
    _inherit = "res.partner"

    is_patient = fields.Boolean(default=False, string="Is Patient")
    is_doctor = fields.Boolean(default=False, string="Is Doctor")
    patient_code = fields.Char(string="Patient Code", readonly=True)
    blood_group = fields.Selection(
        [('a+', 'A+'), ('b+', 'B+'), ('ab+', 'AB+'), ('o+', 'O+'), ('a-', 'A-'), ('b-', 'B-'), ('ab-', 'AB-'),
         ('o-', 'O-')], string="Patient Blood", default='a+')
    height = fields.Float(string="Patient Height")
    weight = fields.Float(string="Patient Weight")
    medical_history = fields.Text(string="Medical_history")
    insurance_document = fields.Binary(string="Insurance_document",attachment=True)
    insurance_filename = fields.Char(string="Insurance_filename")
    last_visit_date = fields.Date(string="Last Visit Date")
    next_visit_datetime = fields.Date(string="Next Visit Datetime")
    emergency_contact_id = fields.Integer(string="Emergency_contact_id")
    risk_level = fields.Selection([('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],string="Risk_level",default='low')

    def generate_code(self):
        if self.id<9:
            self.patient_code='00'+str(self.id)
        elif self.id<99:
            self.patient_code='0'+str(self.id)
        else:
            self.patient_code=str(self.id)

