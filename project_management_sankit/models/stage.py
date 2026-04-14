from odoo import api, fields, models


class DynamicStages(models.Model):
    _name = 'dynamic.stages'
    _description = 'Dynamic Stages'
    _rec_name = 'name'
    _order = 'sequence'


    name = fields.Char(string='Name')
    sequence = fields.Integer(string='Sequence')
    fold = fields.Boolean(string='Folded in Kanban')
    done = fields.Boolean(string='Request Done')
    project_ids = fields.Many2many('project.projects', string='Project Have This', ondelete='restrict')

