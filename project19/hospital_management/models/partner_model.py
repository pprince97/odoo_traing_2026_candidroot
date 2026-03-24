from email.policy import default

from odoo import models, fields, api

class PartnerModel(models.Model):
    _inherit = 'res.partner'

    is_patient=fields.Boolean('Is Patient')
    is_doctor=fields.Boolean('Is Doctor')
    patient_code=fields.Integer('Patient Code',readonly=True,default=000)
    blood_group=fields.Selection([('ap','A+'),('an','A-'),('bp','B+'),('bn','B-'),('abp','AB+'),('abn','AB-'),('op','O+'),('on','O-')],string='Blood Group')
    weight = fields.Float('Weight')
    height = fields.Float('Height')
    medical_history = fields.Text('Medical History')
    insurance_doc = fields.Binary('Insurance Document',attachment=True)
    filename = fields.Char('Insurance Filename')
    last_visit = fields.Date('Last Visit Date')
    next_visit= fields.Datetime('Next Visit Date')
    emergency_contact = fields.Integer('Emergency Contact Number')
    risk_level = fields.Selection([('low','Low'),('medium','Medium'),('high','High')],string='Risk Level')

    appointment_count=fields.Integer('Appointment Count')

    def generate_p_code(self):
        self.patient_code = self.id

    def view_appointment(self):
        appointment = self.env['appointment.model']
        self.appointment_count = appointment.search_count([
            ("partner_id", "=", self.id),
        ])
        return {
            'name': "Appointment",
            'type': 'ir.actions.act_window',
            'view_mode': 'list,form',
            'res_model': 'appointment.model',
            'target': 'self',
            'domain': [
                ("partner_id", "=", self.id),
            ],
        }
