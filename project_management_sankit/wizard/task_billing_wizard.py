from odoo import fields , models , api

class TaskBillingWizard(models.TransientModel):
    _name = "wizard.create_task_bill"
    _description = "Create Task Bill"



    # task_manager_id = fields.Many2one('res.users', string='Manager', readonly=True)

