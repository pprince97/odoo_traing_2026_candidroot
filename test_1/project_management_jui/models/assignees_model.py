from odoo import fields,models,api,Command

class AssigneesModel(models.Model):
    _inherit = 'res.users'

    project_id=fields.Many2one('project.project_jui',string='Project')
    task_id=fields.Many2one('project.task_jui',string='Task')

    @api.model_create_multi
    def create(self, vals):
        res = super().create(vals)
        print(res)
        for rec in res:
            if rec and self.env.context.get('is_assignee'):
                user = self.env['res.users'].search([('id','=',res.id)])
                user.update({'password':'admin','group_ids': [Command.set([self.env.ref('project_management_jui.project_group_assignees').id]),Command.set([self.env.ref('sales_team.group_sale_salesman').id])]})
            if rec and self.env.context.get('is_manager'):
                user = self.env['res.users'].search([('id','=',res.id)])
                user.update({'password':'admin','group_ids': [Command.set([self.env.ref('project_management_jui.project_group_manager').id]),Command.set([self.env.ref('sales_team.group_sale_salesman').id])]})
        return res

