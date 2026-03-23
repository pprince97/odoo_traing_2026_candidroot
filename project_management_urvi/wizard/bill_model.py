from odoo import fields, models, Command


class BillWizard(models.TransientModel):
    _name = 'project.bill.wizard'
    _description = 'Bill Wizard Model'

    choice = fields.Selection([('date_wise', 'Date Wise'), ('task_wise', 'Task Wise')], default='date_wise',
                              string='Choice')
    task_ids = fields.Many2many('project.task.urvi', 'task_bill_rel', 'bill_id', 'task_id', string='Tasks')
    start_date_bill = fields.Datetime('Bill Start Date')
    end_date_bill = fields.Datetime('Bill End Date')
    project_id = fields.Many2one('project.project.urvi', 'Project')

    def wizard_create_bill(self):
        if self.choice == 'date_wise':
            self.task_ids = self.env['project.task.urvi'].search(
                [('done_date', '>=', self.start_date_bill), ('done_date', '<=', self.end_date_bill),
                 ('task_stage.id', '=', self.env.ref('project_management_urvi.stage_demo_done').id),
                 ('project_id', '=', self.project_id.id)])
        l = []
        for i in self.task_ids:
            i.task_stage = self.env.ref('project_management_urvi.stage_demo_invoice').id
            l.append((0, 0, {'name': i.name, 'quantity': 1, 'price_unit': i.total_rate}))
        res = self.env['account.move'].with_context(default_move_type='in_invoice',
                                                    default_project_id=self.project_id.id,
                                                    default_task_ids_=self.task_ids.ids).create(
            {'partner_id': self.project_id.customer_id.id,
             'invoice_date': fields.Date.today(),
             'invoice_line_ids': l
             })
        for rec in res:
            if rec:
                rec.write({'state': 'posted'})
                rec.project_id.bill_count_method()
        return {
            'name': self.project_id.customer_id.name,
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': res.id,
            'target': 'self'
        }

    def create_and_print(self):
        self.ensure_one()
        report_action_v = self.wizard_create_bill()
        return self.env.ref('project_management_urvi.action_report_my_project_bill').report_action(
            report_action_v['res_id'])


class Bill(models.Model):
    _inherit = 'account.move'

    project_id = fields.Many2one('project.project.urvi', 'Project')
    task_ids_ = fields.Many2many('project.task.urvi','task_bill_rel_in','bill_id','task_id',string='Tasks')
