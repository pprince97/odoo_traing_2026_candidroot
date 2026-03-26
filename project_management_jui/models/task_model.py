from odoo import models,fields,api,Command

class TaskModel(models.Model):
    _name='project.task_jui'
    _description='Task Model'

    name=fields.Char(string='Name')

    project_id=fields.Many2one('project.project_jui',string='Project',ondelete='cascade')
    manager_id=fields.Many2one('res.users',string='Manager',related='project_id.manager_id',store=True)
    allowed_assigns = fields.One2many('res.users','task_id',string='Allowed Assignees',compute='_compute_allowed_assigns')
    assignees_id=fields.One2many('res.users','task_id',string='Assignees')

    task_start_date=fields.Date(string='Start Date')
    task_end_date=fields.Date(string='End Date')
    done_date=fields.Date(string='Done Date')

    customer_id=fields.Many2one('res.partner',string='Customer',related='project_id.customer_id',store=True)
    stage_id=fields.Many2one('project.stage',string='Stage',ondelete='cascade')
    timesheet_id=fields.One2many('project.timesheet','task_id',string='Timesheet')

    total_hours=fields.Float(string='Total Hours',compute='_compute_total_hours',store=True,readonly=False)
    bill_count=fields.Integer(string='Bill Count')

    def _compute_allowed_assigns(self):
        if self.project_id:
            l = self.env['project.task_jui'].search(
                [('stage_id.id', 'not in', [self.env.ref('project_management_jui.invoice_demo').id,
                                              self.env.ref(
                                                  'project_management_jui.done_demo').id])]).assignees_id.ids
            self.write({'allowed_assigns': [
                Command.set(list(set(self.project_id.assignees_id.ids) - set(l)))]})
        else:
            self.allowed_assigns = False

    @api.onchange('stage_id')
    def _onchange_stage(self):
        if self.stage_id.id == self.env.ref('project_management_jui.done_demo').id:
            self.done_date = fields.Date.today()

    @api.depends('timesheet_id')
    def _compute_total_hours(self):
        self.total_hours=0
        if self.timesheet_id:
            for rec in self.timesheet_id:
                self.total_hours += rec.spent_hour
        print(self.total_hours)

    def view_bills_task(self):
        self.bill_count = self.env['account.move'].search_count([
            ("task_ids", "in", self.ids),
        ])
        return {
            'name': "Bills",
            'type': 'ir.actions.act_window',
            'view_mode': 'list,form',
            'res_model': 'account.move',
            'target': 'self',
            'domain': [
                ("task_ids", "in", self.ids),
            ],
        }