from datetime import datetime
from datetime import date
from odoo import api, fields, models

class Project(models.Model):
    _name = 'project.projects'
    _description = 'Projects'
    _rec_name = 'name'

    name = fields.Char(string="Name", required=True)
    customer_id = fields.Many2one('res.partner', string="Customer")

    project_manager_id = fields.Many2one('res.users', string='Manager' ,
                                         domain=lambda self: [('group_ids','in',self.env.ref('project_management_sankit.group_project_manager').id)]
                                         )
    project_assignees_ids = fields.Many2many('res.users','project_assignees_user_rel' , 'project_user_id' , 'project_assignees_id' , string='Assignees' ,domain="[('available', '=', True)]")

    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)


    task_ids = fields.One2many('project.tasks', 'project_id',string='Tasks')
    rate_calculation_ids = fields.One2many('project.rate_calculation','projects_id',string="Rate Calculation")
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('in_progress', 'In Progress'),
            ('done', 'Done'),
            ('invoice', 'In Voice'),
        ],
        default='draft',
        string="State",
    )
    def in_progress_state(self):
        self.update({'state':'in_progress'})
    def done_state(self):
        self.update({'state': 'done'})
    def invoice_state(self):
        print("------ ,  , -----")
        self.update({'state': 'invoice'})
    def draft_state(self):
        self.update({'state': 'draft'})

    def action_tasks_button(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Tasks',
            'view_mode': 'list,form',
            'res_model': 'project.tasks',
            'domain': [('project_id', '=', self.id)],
        }



    def _project_update(self, batch_size=100):

       print("---------")
       print(self.task_ids)
