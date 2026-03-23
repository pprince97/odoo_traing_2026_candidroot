from odoo import models,fields,api

class Task(models.Model):
    _name = 'project.tanisha.task'
    _description = 'Project Task'

    name = fields.Char(string='Name')
    project_id = fields.Many2one('project.tanisha.project', string='Project', ondelete='cascade')
    manager_id = fields.Many2one(related='project_id.manager_id',string='Manager')
    assigns = fields.Many2many(related='project_id.assign_ids')
    assign_ids = fields.Many2many('res.users', 'task_user_rel', 'project_id', 'task_id', string='Assigns')
    start_date = fields.Datetime(string='Start Date')
    end_date = fields.Datetime(string='End Date')
    customer_id = fields.Many2one(related='project_id.customer_id',string='Customer')
    stage_id = fields.Many2one('project.stage',string='Stage',ondelete='cascade')
    timesheet_ids = fields.One2many('project.timesheet','task_id',string='Timesheets')
    total_hours = fields.Float(compute='_compute_total_hours', store=True)
    bill_ids = fields.Many2many('project.bill.wizard','task_bill_rel','task_id','bill_id',string='Bill')
    rate = fields.Float(compute='_compute_rate', store=True)
    bill_count = fields.Integer(string='Bill Count')

    @api.depends('timesheet_ids')
    def _compute_total_hours(self):
        for rec in self:
            self.total_hours = sum(rec.timesheet_ids.mapped('spent_hour'))

    @api.depends('total_hours')
    def _compute_rate(self):
        for rec in self:
            rates=rec.project_id.rate_ids
            if rates:
                for r in rates:
                    if r.start_hour<=rec.total_hours<=r.end_hour:
                        rec.rate=r.per_hour_rate
                        break
            else:
                rec.rate=0


    @api.onchange('project_id')
    def _onchange_project_assign(self):
        assigns1 = self.env['project.tanisha.project'].search([('id','=',self.project_id.id)]).assign_ids.ids
        assigns2 = self.env['project.tanisha.task'].search([('stage_id','not in',['Done','Invoice'])]).assign_ids.ids
        self.assigns = list(set(assigns1)-set(assigns2))

    def show_bills(self):
        self.bill_count = self.env['account.move'].search_count([('task_ids','in',self.id)])
        return {
            'type': 'ir.actions.act_window',
            'target': 'self',
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'domain': [('task_ids','in',self.id)],
        }
