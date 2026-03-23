from odoo import models,fields,api
from odoo.exceptions import ValidationError


class Timesheet(models.Model):
    _name = 'project.timesheet'
    _description = 'Project Timesheet'


    task_id = fields.Many2one('project.tanisha.task', string='Task', ondelete='cascade')
    assigns = fields.Many2many(related='task_id.assign_ids',string='Assigns')
    assign_id = fields.Many2one('res.users',string='Assign',ondelete='cascade')
    start_date = fields.Datetime(string='Start Date')
    end_date = fields.Datetime(string='End Date')
    description = fields.Text(string='Description')
    spent_hour = fields.Float(string='Spent Hour',compute='_compute_spent_hour',store=True)

    @api.depends('start_date','end_date')
    def _compute_spent_hour(self):
        if self.start_date and self.end_date:
            if self.start_date < self.end_date:
                self.spent_hour = (self.end_date - self.start_date).total_seconds()/3600.00
            else:
                raise ValidationError("Start datetime must be before end datetime!!!!!")


