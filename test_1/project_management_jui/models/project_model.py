from odoo import models, api, fields

class ProjectModel(models.Model):
    _name = 'project.project_jui'
    _description = 'Project Model'

    name=fields.Char(string='Project Name')
    manager_id=fields.Many2one('res.users',string='Manager Name',ondelete='cascade',context={'is_manager':True},domain=lambda self: [('group_ids', 'in', self.env.ref('project_management_jui.project_group_manager').id)])
    assignees_id=fields.One2many('res.users','project_id',string='Assignees',context={'is_assignee':True},domain=lambda self: [('group_ids', 'not in', self.env.ref('project_management_jui.project_group_admin').id)])
    start_date=fields.Date(string='Start Date')
    end_date=fields.Date(string='End Date')
    per_hour_rate_ids=fields.Many2many('project.hour_rate','project_hour_rate_relation','project_id','hour_rate_id',string='Per Hour Rate')
    state=fields.Selection([('new','New'),('in_progress','In Progress'),('done','Done'),('cancelled','Cancelled')],string='State',default='new')
    customer_id=fields.Many2one('res.partner',string='Customer',ondelete='cascade')
    task_count = fields.Integer(string='Task Count')
    bill_count = fields.Integer(string='Bill Count')
    bill_show = fields.Boolean(string='Bill Show', compute='_show_bill')

    def _show_bill(self):
        self.bill_show = self.env['ir.config_parameter'].sudo().get_param('project_management_jui.show_bill')
        print(self.bill_show)

    def create_bill(self):
        self.bill_show = self.env['ir.config_parameter'].sudo().get_param('project_management_jui.show_bill')
        if self.bill_show:
            return{
                'name': 'Bill',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'bill.wizard',
                'target': 'new',
                'context':{'default_project_id':self.id}
            }
        else:
            return None

    def view_tasks(self):
        self.task_count = self.env['project.task_jui'].search_count([
            ("project_id", "=", self.id),
        ])
        return {
            'name': "Tasks",
            'type': 'ir.actions.act_window',
            'view_mode': 'list,form',
            'res_model': 'project.task_jui',
            'target': 'self',
            'domain': [
                ("project_id", "=", self.id),
            ],
            'context': {'default_project_id': self.id}
        }

    def view_bills(self):
        self.bill_count=self.env['account.move'].search_count([
            ("project_id", "=", self.id),
        ])
        return {
            'name': "Bills",
            'type': 'ir.actions.act_window',
            'view_mode': 'list,form',
            'res_model': 'account.move',
            'target': 'self',
            'domain': [
                ("project_id", "=", self.id),
            ],
        }

    def scheduled_action_project(self):
        print(self)
