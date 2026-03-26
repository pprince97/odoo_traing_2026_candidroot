from odoo import api, fields,models

class DepartmentModel(models.Model):
    _name = 'department.model'
    _description='Department description'

    name=fields.Char(string='Name')
    color = fields.Integer(string='Color')
    # hospital_ids = fields.Many2many('hospital.model','hospital_department_relation','department_id','hospital_id',string='Hospital',invisible=True)
    # doctor_ids = fields.One2many('res.partner','department_id',string='Doctors',invisible=True)