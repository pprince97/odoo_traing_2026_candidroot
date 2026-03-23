from odoo import models,fields

class Department(models.Model):
    _name = "hospital.department"
    _description = "Department Model"

    name = fields.Char(string="Name")
    color = fields.Integer(string="Color")
    # patient_ids = fields.Many2many('res.partner','dep_patient_rel','department_id','patient_id',string="patient")
    hospital_ids = fields.Many2many('hospital.hospital', 'hospital_department_rel', 'department_id', 'hospital_id',
                                      string='Departments')