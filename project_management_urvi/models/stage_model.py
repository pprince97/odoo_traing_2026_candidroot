from odoo import models,fields

class Stage(models.Model):
    _name = 'project.stage'
    _description = 'Stage Model'

    name = fields.Char(string='Stage Name')
    project_ids = fields.Many2many('project.project.urvi','stage_project_rel','stage_id','project_id',string='Projects')
    fold_state = fields.Boolean(string='Fold State')