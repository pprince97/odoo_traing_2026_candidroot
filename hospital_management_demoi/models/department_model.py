from odoo import models,fields,api

class Department(models.Model):
    _inherit = "hr.department"

    # department_name = fields.Char(string="Department Name")
    department_floor = fields.Char(string="Department Floor")
    department_phone = fields.Integer(string="Department Phone")
    is_active = fields.Boolean(string="Is Active")
    capacity = fields.Integer(string="Capacity")
    description = fields.Text(string="Description")
    hospital_ids = fields.Many2many('hospital.hospital','hos_dep_rel','department_id','hospital_id',string='Department')
    appointment_ids = fields.One2many("hospital.appointment","department_id",string="Appointment")
    doctor_ids = fields.One2many('hospital.doctor',"department_id",string="Doctor")