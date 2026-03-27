from odoo import models,fields,api
from dateutil.relativedelta import relativedelta

class ProjectTimesheet(models.Model):
    _name = 'project.timesheet'
    _description = 'Project TimeSheet'
    _rec_name = 'task_id'

    start_date = fields.Datetime(string='Start DateTime',required=True)
    end_date = fields.Datetime(string='End DateTime',required=True)
    description = fields.Text(string='Description')
    hours_spent = fields.Float(string='Hours Spent',compute='_compute_hours_spent',store=True)
    task_id = fields.Many2one('project.tasks',string='Task')
    assignee_id = fields.Many2one('res.users',string='Assignees')
    allowed_assignees = fields.Many2many('res.users',string='Allowed Assignees',compute='_compute_allowed_assignees')
    amount = fields.Float(string='Amount')
    per_hour_chargee = fields.Float(string='Charge Hours Spent')


    @api.depends('task_id')
    def _compute_allowed_assignees(self):
        for record in self:
            if record.task_id:
                record.allowed_assignees = record.task_id.assignee_ids
                # print('>>>>>>>>>>>>>>>>>..',record.allowed_assignees)
            else:
                record.allowed_assignees = self.env['res.users']

    @api.depends('start_date','end_date')
    def _compute_hours_spent(self):
        for project in self:
            if project.start_date and project.end_date and project.start_date <= project.end_date:
                diff = relativedelta(project.end_date, project.start_date)
                project.hours_spent = (diff.days * 24) + diff.hours + (diff.minutes / 60)
            else:
                project.hours_spent = 0

    @api.onchange('start_date','end_date')
    def _onchange_hours_spent(self):
        for record in self:
            per_hr_rt = record.env['project.per.hour.rate'].search([
                ('project_id', '=',record.task_id.project_id.id),
                ('start_hours','<',record.hours_spent),
                ('end_hours','>=',record.hours_spent),
            ],limit=1).per_hour_rate
            record.per_hour_chargee = per_hr_rt
            record.amount = per_hr_rt * record.hours_spent

