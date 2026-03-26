from odoo import api,fields,models

class BillModel(models.Model):
    _inherit = 'account.move'

    project_id = fields.Many2one('project.project_jui',string='Project',ondelete='cascade')
    task_ids = fields.Many2many('project.task_jui','bill_task_rel','bill_id','task_id',string='Tasks')