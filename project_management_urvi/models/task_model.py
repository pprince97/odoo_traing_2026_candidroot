from odoo import models, fields, api, Command


class Task(models.Model):
    _name = 'project.task.urvi'
    _description = 'Task Model'

    name = fields.Char(string='Task Name')
    project_id = fields.Many2one('project.project.urvi', string='Projects', ondelete='cascade')
    manager_id = fields.Many2one('res.users', related='project_id.manager_id', string='Manager', ondelete='cascade',
                                 store=True)
    assigns_ids = fields.Many2many('res.users', string='Assigns')
    task_start_date = fields.Datetime(string='Start Date')
    task_end_date = fields.Datetime(string='End Date')
    task_stage = fields.Many2one('project.stage', string='Task Status')
    timesheet = fields.One2many('project.timesheet', 'task_id', string='Timesheet')
    customer_id = fields.Many2one('res.partner', related='project_id.customer_id', string='Customer', store=True)
    # bill_id = fields.Many2one('project.bill.wizard',string='Bill',ondelete='cascade')

    allowed_assigns = fields.Many2many('res.users', string='Allowed', compute='_compute_allowed_assigns')
    total_time = fields.Float(string='Total Time', compute='_compute_total_time', store=True)
    done_date = fields.Datetime(string='Done Date', compute='_compute_done_date', store=True, readonly=False)
    total_rate = fields.Float(string='Total Rate', compute='_compute_total_rate', store=True)
    bill_count = fields.Integer(string='Bill Count',compute='_compute_bill_count', store=True, readonly=False)
    bill_ids = fields.Many2many('account.move','task_bill_rel_in','task_id','bill_id', string='Bill IDs')

    @api.depends('project_id')
    def _compute_allowed_assigns(self):
        if self.project_id:
            l = self.env['project.task.urvi'].search(
                [('task_stage.id', 'not in', [self.env.ref('project_management_urvi.stage_demo_invoice').id, self.env.ref('project_management_urvi.stage_demo_done').id])]).assigns_ids.ids
            self.write({'allowed_assigns': [
                Command.set(list(set(self.project_id.assigns_ids.ids) - set(l)))]})
        else:
            self.allowed_assigns = False

    @api.depends('timesheet')
    def _compute_total_time(self):
        self.total_time = 0
        for rec in self:
            if rec.timesheet:
                print(rec)
                for task in rec.timesheet:
                    rec.total_time += float(task.spent_hour)

    @api.depends('task_stage')
    def _compute_done_date(self):
        for rec in self:
            if rec.task_stage.id==self.env.ref('project_management_urvi.stage_demo_done').id:
                print('>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                rec.done_date = fields.Datetime.now()
            else:
                rec.done_date = False
            print('>>>>>>>>>>>>>>>>>>>>>>',rec.done_date)

    @api.depends('timesheet')
    def _compute_total_rate(self):
        self.total_rate = 0
        for rec in self:
            if rec.timesheet:
                rec.total_rate = sum(sheet.rate for sheet in rec.timesheet)

    @api.depends('bill_ids')
    def _compute_bill_count(self):
        self.bill_count = self.env['account.move'].search_count(
            [('task_ids_', 'in', self.ids)])

    def bill_count_task(self):
        a = {
            'name': self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'domain': [('task_ids_', 'in', self.ids)],
            'target': 'self'
        }
        if self.bill_count == 1:
            a['view_mode'] = 'form'
            a['res_id'] = (self.env['account.move'].search(
                [('task_ids_', 'in', self.ids)])).id
        return a

    # l=[]
    # for rec in s:
    #     l.extend(rec.assigns_ids.ids)