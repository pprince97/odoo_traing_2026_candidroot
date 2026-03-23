from odoo import models, fields


class Project(models.Model):
    _name = 'project.project.urvi'
    _description = 'Project Model'

    name = fields.Char(string='Project Name')
    manager_id = fields.Many2one('res.users', string='Manager', ondelete='cascade',
                                 domain=lambda self: [
                                     ('group_ids', 'in',
                                      self.env.ref('project_management_urvi.group_project_manager').id)
                                 ])
    assigns_ids = fields.Many2many('res.users', 'user_assigns_rel', 'assigns_id', 'user_id', string='Assigns')
    start_date = fields.Datetime(string='Start Date')
    end_date = fields.Datetime(string='End Date')
    per_hours_rate = fields.Many2many('project.hours.rate', 'project_hours_rel', 'project_id', 'hours_rate_id',
                                      string='PerHours Rate')
    state = fields.Selection([('new', 'New'), ('in_progress', 'In Progress'), ('done', 'Done'), ('cancel', 'Cancel')],
                             string='Status')
    customer_id = fields.Many2one(comodel_name='res.partner', string='Customer')
    bill_count = fields.Integer(string='Bill Count')
    system_para = fields.Boolean(string='System Para', compute='_compute_system_para_bool')

    def _compute_system_para_bool(self):
        print('>>>>>>>>>>>>', self.system_para)
        self.system_para = self.env['ir.config_parameter'].get_param('project_management_urvi.project_bill')
        print('>>>>>>>>>>>>', self.system_para)

    def create_bill(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'project.bill.wizard',
            'view_mode': 'form',
            'context': {'default_project_id': self.id},
            'target': 'new'
        }

    def bill_count_method(self):
        # print('>>>>>>>>>>>>>>>>>>>',self.env.context.get('project'))
        self.bill_count = self.env['account.move'].search_count(
            [('project_id', '=', self.id)])
        a = {
            'name': self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'domain': [('project_id', '=', self.id)],
            'target': 'self'
        }
        if self.bill_count == 1:
            a['view_mode'] = 'form'
            a['res_id'] = (self.env['account.move'].search(
                [('project_id', '=', self.id)])).id
        return a


    def schedule_method_act(self):
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>schedule')