from odoo import models,fields,api

class Departments(models.Model):
    _name = 'hospital.management.departments'
    _description = 'Departments'

    name = fields.Char(string='Name',required=True)
    dept_code = fields.Char(string='Dept Code')
    hospital_ids =fields.Many2many('hospital.management.hospitals','hospital_department_rel','department_id','hospital_id',string='Departments')
    doctor_ids = fields.One2many('res.partner','department_id',string='Doctors')