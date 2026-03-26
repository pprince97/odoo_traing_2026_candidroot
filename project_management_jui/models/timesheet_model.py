from odoo import fields,models,api

class TimesheetModel(models.Model):
    _name='project.timesheet'
    _description='Timesheet Model'

    task_id=fields.Many2one('project.task_jui',string='Task',ondelete='cascade')
    assignees_id=fields.Many2one('res.users',string='Assignees',ondelete='cascade')
    start_date=fields.Datetime(string='Start Date')
    end_date=fields.Datetime(string='End Date')
    description=fields.Text(string='Description')
    spent_hour=fields.Float(string='Spent Hour',compute='_compute_spent_hour',store=True)

    @api.depends('start_date', 'end_date')
    def _compute_spent_hour(self):
        for rec in self:
            if rec.start_date and rec.end_date:
                diff = rec.end_date-rec.start_date
                rec.spent_hour = diff.total_seconds()/3600



