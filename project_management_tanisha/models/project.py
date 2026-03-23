from odoo import models,fields,api

class Project(models.Model):
    _name = 'project.tanisha.project'
    _description = 'Project'

    name = fields.Char(string='Name')
    manager_id = fields.Many2one('res.users',string='Manager',ondelete='cascade')
    assign_ids = fields.Many2many('res.users','project_user_rel','project_id','user_id',string='Assigns')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    rate_ids = fields.Many2many('project.hour.rate','project_rate_rel','project_id','rate_id',string='Rates')
    state = fields.Selection([('new','New'),('in_progress','In Progress'),('done','Done'),('cancel','Cancel')],string='State',default='new')
    customer_id = fields.Many2one('res.partner',string='Customer')
    stage_ids = fields.Many2many('project.stage','stage_project_rel','project_id','stage_id',string='Stages')
    task_ids = fields.One2many('project.tanisha.task','project_id',string='Tasks')
    bill_count = fields.Integer(string='Bill Count')

    def generate_bill(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'project.bill.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_project_id': self.id},
        }

    def show_bills(self):
        self.bill_count = self.env['account.move'].search_count([('project_id','=',self.id)])
        return {
            'type': 'ir.actions.act_window',
            'target': 'self',
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'domain': [('project_id','=',self.id)],
        }

class AccountMove(models.Model):
    _inherit = ['account.move']
    project_id = fields.Many2one('project.tanisha.project',string='Project')
    task_ids = fields.Many2many('project.tanisha.task',string='Task')


