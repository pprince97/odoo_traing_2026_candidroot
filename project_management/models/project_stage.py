from odoo import models,fields,api

class ProjectStage(models.Model):
    _name = 'project.stage'
    _description = 'Project Stage'

    name = fields.Char(string='Project Stages',required=True)
    project_ids = fields.Many2many('project.projects','stage_project_rel','stage_id','project_id',string='Projects')
    fold=fields.Boolean('Fold')