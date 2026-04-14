from odoo import fields , models , api

class Department(models.Model):
    _name = 'hospital.department'
    _rec_name = 'department_name'

    department_name = fields.Char(string='Name', required=True)
    hospital_ids = fields.Many2many('hospital.hospital' , 'hospital_department_rel','department_id' ,'hospital_id' ,string='Hospitals')
    doctor_ids = fields.One2many('res.partner', 'department_id', string="Doctor")