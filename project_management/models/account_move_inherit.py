from odoo import models, fields

class InheritAccountMove(models.Model):
    _inherit = 'account.move'

    project_id = fields.Many2one('project.projects','Projects')
    task_ids = fields.One2many('project.tasks','bill_id','Tasks')