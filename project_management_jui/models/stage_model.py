from odoo import fields,models,api

class StageModel(models.Model):
    _name='project.stage'
    _description='Stage Model'

    name=fields.Char(string='Stage Name')
    project_ids=fields.Many2many('project.project_jui','project_stage_relation','stage_id','project_id',string='Project',ondelete='cascade')
    fold=fields.Boolean(string='Fold')

    @api.model_create_multi
    def create(self, vals):
        res = super(StageModel, self).create(vals)
        for rec in res:
            if rec.env.context.get('default_project_ids'):
                rec.project_ids = rec.env.context.get('default_project_ids')
        return res
