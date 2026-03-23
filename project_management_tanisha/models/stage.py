from odoo import models,fields,api

class Stage(models.Model):
    _name = 'project.stage'
    _description = 'Project Stage'

    name = fields.Char(string='Name')
    project_ids = fields.Many2many('project.tanisha.project','stage_project_rel','stage_id','project_id',string='Projects')
    task_ids = fields.One2many('project.tanisha.task','stage_id',string='Tasks')
    fold = fields.Boolean(string='Make Foldable? ', default=False)