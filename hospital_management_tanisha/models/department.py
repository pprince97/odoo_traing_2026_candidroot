from odoo import models, fields, api

class Department(models.Model):
    _name = 'hospital.department'
    _description = 'Department'

    name = fields.Char(string='Name')
    hospital_ids = fields.Many2many('hospital.hospital', 'hospital_department_rel', 'department_id', 'hospital_id',string='Hospitals')
    doctor_ids = fields.One2many('res.partner', 'department_id', string='Doctors')
    appointment_ids = fields.One2many('hospital.appointment', 'department_id', string='Appointments')
