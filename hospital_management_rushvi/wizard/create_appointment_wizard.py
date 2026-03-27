from odoo import models,fields,api

class CreateAppointmentWizard(models.TransientModel):
    _name = 'wizard.create.appointment.wizard'
    _description = 'Create Appointment Wizard'

    hospital_id = fields.Many2one('hospital.management.hospitals',string='Hospital')
    patient_id = fields.Many2one('res.partner',string='Patient',domain=[('patient_code','ilike','P%')])
    department_id = fields.Many2one('hospital.management.departments',string='Department')
    doctor_id = fields.Many2one('res.partner',string='Doctor',domain="[('doctor_code','ilike','D%')]")

    def create_appointment(self):
        return self.env['hospital.management.appointments'].create({
            'hospital_id': self.hospital_id.id,
            'patient_id': self.patient_id.id,
            'department_id': self.department_id.id,
            'doctor_id': self.doctor_id.id,
        })

    @api.model
    def default_get(self, fields):
        print('???????????????????????????',fields)
        res = super(CreateAppointmentWizard, self).default_get(fields)
        patient_id = self.env.context.get('active_id')
        if patient_id:
            res['patient_id'] = patient_id
        return res