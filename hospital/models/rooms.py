from odoo import models,fields,api

class Rooms(models.Model):
    _name='rooms.obj'
    _description='Rooms'
    _rec_name='number'

    number=fields.Integer(string='Room Number')
    type=fields.Selection([('general','General'),('private','Private')],string='Room Type')
    no_beds=fields.Integer(string='Number of Beds')
    is_available=fields.Boolean(string='Is Available')
    cost_room=fields.Float(string='Cost of room per day',readonly=True)

    room_d=fields.Datetime('Room Date')
    p_id=fields.Many2many('patient.obj','patient_room_rel','room_id','patient_id',string='Patients')