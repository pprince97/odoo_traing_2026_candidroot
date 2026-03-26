from odoo import models,fields,api

class Patients(models.Model):
    _name='patient.obj'
    _description='Patients'
    _inherit=['mail.thread','mail.activity.mixin']

    name=fields.Char('Name',required=True,tracking=True)
    age=fields.Integer('Age')
    dob=fields.Date('Date of Birth')
    blood_group=fields.Selection([('ap','A+'),('an','A-'),('bp','B+'),('bn','B-'),('abp','AB+'),('abn','AB-'),('op','O+'),('on','O-')],string='Blood Group')
    gender=fields.Selection([('male','Male'),('female','Female')],string='Gender')
    address=fields.Text('Address')
    weight=fields.Float('Weight')
    height=fields.Float('Height')
    contact=fields.Integer('Contact Details')
    emergency_contact=fields.Integer('Emergency Contact')
    p_report=fields.Binary('Previous consultancy report')
    file_name= fields.Char(string='File Name')

    illness=fields.Char('Illness Details')
    department=fields.Char('Department')

    doctor=fields.Many2one('hr.employee',string='Doctor',ondelete='cascade')
    appointment=fields.One2many('appointment.obj','p_id',string='Appointments')
    r_id=fields.Many2many('rooms.obj','patient_room_rel','patient_id','room_id',string='Rooms')

    date_start=fields.Datetime('Date of Start',invisible=True)