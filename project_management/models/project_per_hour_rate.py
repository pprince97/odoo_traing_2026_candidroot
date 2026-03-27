from odoo import models,fields,api

class ProjectTask(models.Model):
    _name = 'project.per.hour.rate'
    _description = 'Project Per Hour Rate'

    start_hours = fields.Integer('Start Hours')
    end_hours = fields.Integer('End Hours')
    per_hour_rate = fields.Float('Per Hour Rate')
    project_id = fields.Many2one('project.projects',string='Project')
