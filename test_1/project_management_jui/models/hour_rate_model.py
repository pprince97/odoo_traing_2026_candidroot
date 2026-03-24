from odoo import api,fields,models

class HourRateModel(models.Model):
    _name='project.hour_rate'
    _description='Per Hours Rate Model'

    name=fields.Char(string='Name')
    start_range=fields.Integer(string='Start Of The Range')
    end_range=fields.Integer(string='End Of The Range')
    per_hour_rate=fields.Float(string='Per Hour Rate')