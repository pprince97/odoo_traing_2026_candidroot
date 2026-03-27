from odoo import models,fields,api



class ProjectProject(models.Model):
    _name = 'project.projects'
    _description = 'Project'

    name = fields.Char(string='Project Name',required=True)
    manager_id =fields.Many2one('res.users',string='Manager',required=True,
                                domain=lambda self: [('group_ids','in', self.env.ref('project_management.group_project_manager').id)])
    assignee_ids = fields.Many2many('res.users','project_assignee_rel','project_id','assignee_id',string='Assignee',
                                    domain=lambda self: [('group_ids','!=', self.env.ref('project_management.group_project_admin').id)])
    start_date = fields.Datetime(string='Start Date',required=True)
    end_date = fields.Datetime(string='End Date',required=True)
    state = fields.Selection([('new','New'),('in_progress','In Progress'),('done','Done'),('cancelled','Canceled')],string='Status',default='new')
    customer_id = fields.Many2one('res.partner',string='Customer',required=True)
    stage_ids = fields.Many2many('project.stage','stage_project_rel','project_id','stage_id',string='Stage')
    task_count = fields.Integer(string='Task Count',compute='_compute_task_count')
    task_ids = fields.One2many('project.tasks','project_id',string='Tasks')
    per_hour_rate = fields.One2many('project.per.hour.rate','project_id',string='Rate')
    bill_ids = fields.One2many('account.move','project_id',string='Bills')
    bill_count = fields.Integer(string='Bill Count',compute='_compute_bill_count')
    show_generate_bill_button = fields.Boolean(string='Show Generate Bill Button',compute='_compute_show_bill_button')

    def state_in_progress(self):
        self.state = 'in_progress'

    def state_canceled(self):
        self.state = 'cancelled'

    def state_done(self):
        self.state = 'done'

    @api.depends('task_ids')
    def _compute_task_count(self):
        for record in self:
            record.task_count = len(record.task_ids)

    def view_tasks(self):
        return {
            'name': 'Tasks',
            'type': 'ir.actions.act_window',
            'res_model': 'project.tasks',
            'view_mode': 'list,form',
            'domain': [('project_id','=',self.id)],
            'target': 'current',
            'context': {'default_project_id': self.id},
        }

    def generate_bill(self):
        return {
            'name': 'Bill',
            'type': 'ir.actions.act_window',
            'res_model': 'wizard.bill.generation',
            'view_mode': 'form',
            'context': {'default_project_id': self.id},
            'target': 'new',
        }

    @api.depends('bill_ids')
    def _compute_bill_count(self):
        for record in self:
            record.bill_count = len(record.bill_ids)

    def view_bills(self):
        return {
            'name': 'Bills',
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'domain': [('project_id', '=', self.id)],
            'target': 'current',
        }

    def _schedule_action_demo(self):
        print("\n\n\n\nHii Schedule Demo")
        return None

    def _compute_show_bill_button(self):
        show_btn = self.env['ir.config_parameter'].sudo().get_param('project_management.test_demo')
        for record in self:
            record.show_generate_bill_button = show_btn