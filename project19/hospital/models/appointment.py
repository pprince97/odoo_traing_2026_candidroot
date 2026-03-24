from odoo import models,fields,api

class Appointment(models.Model):
    _name='appointment.obj'
    _description='Appointments'
    _rec_name='appointment'

    appointment=fields.Datetime('Appointment',required=True)
    status=fields.Selection([('book','Book'),('Pending','Pending'),('confirmed','Confirmed'),('cancelled','Cancelled')], 'Status',default='book')
    p_id=fields.Many2one('patient.obj','Patient',ondelete='cascade')
    d_id=fields.Many2one('hr.employee','Doctor',ondelete='cascade')