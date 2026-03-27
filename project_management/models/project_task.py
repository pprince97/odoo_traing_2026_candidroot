from http.cookiejar import domain_match

from odoo import models,fields,api

class ProjectTask(models.Model):
    _name = 'project.tasks'
    _description = 'Project Task'
    _rec_name = 'task_name'

    task_name = fields.Char(string='Task Name',required=True)
    project_id = fields.Many2one('project.projects',required=True)
    manager_id = fields.Many2one('res.users')
    customer_id = fields.Many2one('res.partner','Customer')
    assignee_ids = fields.Many2many('res.users','task_assignees_rel','task_id','assignee_id',string='Assignees')
    task_start_date = fields.Datetime(string='Start Date',default=fields.Datetime.now())
    task_end_date = fields.Datetime(string='End Date')
    task_done_date = fields.Datetime(string='Done Date')
    timesheet_ids = fields.One2many('project.timesheet','task_id',string='Timesheet')
    stage_id = fields.Many2one('project.stage',string="Stage",domain="['|',('project_ids', '=', project_id),('project_ids', '=', False)]" )
    task_hours = fields.Float(compute='_compute_task_hours',string="Total Hours")
    task_total_cost = fields.Float(compute='_compute_task_cost',string="Total Amount")
    bill_id = fields.Many2one('account.move',string="Bill")
    bill_count = fields.Integer(string='Bill Count',compute='_compute_bill_count')

    allowed_assignees = fields.Many2many('res.users', string="Allowed Assignees",compute="_compute_allowed_assignees",store=True,readonly=False  )

    @api.depends('project_id', 'project_id.task_ids.stage_id', 'project_id.assignee_ids')
    def _compute_allowed_assignees(self):
        done_invoice_stage_ids = [
            self.env.ref('project_management.stage6_demo').id,
            self.env.ref('project_management.stage5_demo').id
        ]
        for record in self:
            if not record.project_id:
                record.allowed_assignees = self.env['res.users']
                continue
            busy_tasks = record.project_id.task_ids.filtered(
                lambda t: t.stage_id.id not in done_invoice_stage_ids
            )
            busy_assignee_ids = busy_tasks.mapped('assignee_ids').ids
            all_possible_assignees = record.project_id.mapped('assignee_ids')
            record.allowed_assignees = all_possible_assignees.filtered(
                lambda u: u.id not in busy_assignee_ids
            )

    @api.onchange('project_id')
    def _onchange_project_id(self):
        for record in self:
            if record.project_id:
                record.manager_id = record.project_id.manager_id
                record.customer_id = record.project_id.customer_id
                record.assignee_ids = [(5, 0, 0)]
            else:
                record.manager_id = False
                record.customer_id = False
                record.assignee_ids = [(5, 0, 0)]

    @api.depends('timesheet_ids')
    def _compute_task_hours(self):
        for record in self:
            if record.timesheet_ids:
                record.task_hours = sum(record.timesheet_ids.mapped('hours_spent'))
            else:
                record.task_hours = 0

    @api.depends('timesheet_ids')
    def _compute_task_cost(self):
        for record in self:
            if record.timesheet_ids:
                record.task_total_cost = sum(record.timesheet_ids.mapped('amount'))
            else:
                record.task_total_cost = 0

    @api.onchange('stage_id')
    def _onchange_stage_id(self):
        for record in self:
            if record.stage_id and record.stage_id == self.env.ref('project_management.stage6_demo'):
                record.task_done_date = fields.Datetime.now()

    @api.depends('stage_id')
    def _compute_bill_count(self):
        for record in self:
            record.bill_count = len(record.bill_id)

    def view_bills(self):
        return {
            'name': 'Bill',
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'domain': [('project_id', '=', self.project_id.id),('task_ids','in',self.id)],
            'target': 'current',
        }

    # @api.depends('project_id','project_id.assignee_ids','project_id.task_ids.stage_id','project_id.task_ids.assignee_ids')
    # def _compute_allowed_assignees(self):
    #     stage_ids = [
    #         self.env.ref('project_management.stage6_demo').id,
    #         self.env.ref('project_management.stage5_demo').id
    #     ]
    #     for record in self:
    #         if record.project_id:
    #             project_users = record.project_id.assignee_ids
    #             matching_tasks = record.project_id.task_ids.filtered(
    #                 lambda t: t.stage_id.id in stage_ids
    #             )
    #             not_busy_users = matching_tasks.mapped('assignee_ids')
    #             record.allowed_assignees = project_users & not_busy_users
    #         else:
    #             record.allowed_assignees = self.env['res.users'].search([]).mapped('assignee_ids')