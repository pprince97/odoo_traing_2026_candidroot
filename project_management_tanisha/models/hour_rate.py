from odoo import models,fields,api
from odoo.exceptions import ValidationError

class HourRate(models.Model):
    _name = 'project.hour.rate'
    _description = 'Hour Rate'

    start_hour = fields.Float(string='Starting Hour')
    end_hour = fields.Float(string='Ending Hour')
    per_hour_rate = fields.Float(string='Per hour Rate')
    project_ids = fields.Many2many('project.tanisha.project','project_rate_rel','rate_id','project_id',string='Projects')
