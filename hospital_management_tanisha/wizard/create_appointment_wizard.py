from odoo import models,fields,api,_

from odoo.exceptions import ValidationError

from odoo.fields import Command


class AppointmentWizard(models.TransientModel):
    _name = 'create.appointment.wizard'
    _description = 'Create Appointment Wizard'

    hospital_id = fields.Many2one('hospital.hospital', string='Hospital')
    patient_id = fields.Many2one('res.partner', string='Patient', domain="[('patient_id','ilike','P%')]")
    department_id = fields.Many2one('hospital.department', string='Department')
    doctor_id = fields.Many2one('res.partner', string='Doctor', domain="[('doctor_id','ilike','D%')]")
    appointment_date = fields.Date(string='Appointment Date', default=fields.Date.today())

    @api.model
    def default_get(self, fields):
        results = super().default_get(fields)
        patient_id = self.env.context.get('active_id')
        if patient_id:
            results['patient_id'] = patient_id
        return results

    def create_appointment_wizard(self):
        res = self.env['hospital.appointment'].create({
            'hospital_id': self.hospital_id.id,
            'patient_id': self.patient_id.id,
            'department_id': self.department_id.id,
            'doctor_id': self.doctor_id.id,
            'appointment_date': self.appointment_date,
        })
        return res

    @api.onchange('appointment_date')
    def _onchange_appointment_date(self):
        for rec in self:
            if rec.appointment_date and rec.appointment_date < fields.Date.today():
                raise ValidationError(_("Appointment date cannot be in past!!!!!!"))