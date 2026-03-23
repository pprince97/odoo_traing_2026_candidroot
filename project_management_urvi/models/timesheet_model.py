from odoo import models,fields,api
from odoo.exceptions import ValidationError


class Timesheet(models.Model):
    _name = 'project.timesheet'
    _description = 'Timesheet Model'
    _rec_name = 'assignee'

    task_id = fields.Many2one('project.task.urvi',string='Task',ondelete='cascade')
    allowed_assigns = fields.Many2many('res.users',related='task_id.assigns_ids',string='Assigns')
    assignee = fields.Many2one('res.users',string='Assignee')
    t_start_date = fields.Datetime(string='Start Date')
    t_end_date = fields.Datetime(string='End Date')
    description = fields.Char(string='Description')
    spent_hour = fields.Float(string='Spent Hour',compute='_compute_spent_hour',store=True)
    rate = fields.Float(string='Rate',compute='_compute_rate',store=True)

    @api.depends('t_start_date','t_end_date')
    def _compute_spent_hour(self):
        for rec in self:
            if rec.t_start_date and rec.t_end_date:
                diff = rec.t_end_date - rec.t_start_date
                rec.spent_hour = diff.total_seconds()/3600.00

    @api.onchange('t_end_date')
    def _onchange_t_end_date(self):
        for rec in self:
            if rec.t_end_date and rec.t_start_date and rec.t_end_date > rec.t_start_date:
                pass
            else:
                raise ValidationError("Invalid start date or end date")

    @api.depends('spent_hour')
    def _compute_rate(self):
        for rec in self:
            t = self.env['project.project.urvi'].search([('id','=',rec.task_id.project_id.id)])
            for i in t.per_hours_rate:
                if rec.spent_hour and ((rec.spent_hour>=i.s_hour) and (rec.spent_hour<=i.e_hour)):
                    rec.rate = i.rate * rec.spent_hour
                    break
            else:
                rec.rate = 1000*rec.spent_hour




