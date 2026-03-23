from odoo import models,fields,api

class Hospital(models.Model):
    _name = 'hospital.hospital'
    _description = 'Hospital'

    name = fields.Char(string='Name')
    address = fields.Char(string='Address')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    registration_no = fields.Char(string='Registration Number')
    description = fields.Text(string='Description')
    department_ids = fields.Many2many('hospital.department', 'hospital_department_rel', 'hospital_id', 'department_id',string='Departments')
    appointment_ids = fields.One2many('hospital.appointment', 'hospital_id', string='Appointments')
    doctor_ids = fields.Many2many('res.partner', 'hospital_doctor_rel', 'hospital_id', 'doctor_id', string='Doctors', domain="[('doctor_id','ilike','D%')]")
    patient_ids = fields.Many2many('res.partner', 'hospital_patient_rel','hospital_id', 'patient_id',string='Patients', domain="[('patient_id','ilike','P%')]")

    def create_department(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'create.department.wizard',
            'view_mode': 'form',
            'target': 'new',
        }

    # @api.onchange('department_ids')
    # def _onchange_department(self):
    #     self.appointment_ids = self.env['hospital.appointment'].search([('department_id','in',self.department_ids.ids)])
    #     self.doctor_ids = self.env['res.partner'].search([('doctor_id','in',self.appointment_ids.ids)])
    #     self.patient_ids = self.env['res.partner'].search([('patient_id','in',self.doctor_ids.ids)])



