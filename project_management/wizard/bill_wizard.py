from odoo import models,fields,api
from odoo.exceptions import ValidationError

class CreateAppointmentWizard(models.TransientModel):
    _name = 'wizard.bill.generation'
    _description = 'Generate Bill'

    bill_type = fields.Selection([('date_wise','Date Wise'),('task_wise','Task Wise')])
    start_date = fields.Datetime(string='Start Date')
    end_date = fields.Datetime(string='End Date')
    task_ids = fields.Many2many('project.tasks','task_bill_rel','bill_id','task_id',string='Tasks')
    project_id = fields.Many2one('project.projects','Project')

    def generate_bill(self):
        if self.bill_type=='task_wise':
            done_tasks = self.task_ids
        else:
            done_tasks = self.env['project.tasks'].search([('stage_id.name', '=', 'Done'),
                                                           ('project_id','=',self.project_id),
                                                           ('task_done_date','>=',self.start_date),
                                                           ('task_done_date','<=',self.end_date)])
            if not done_tasks:
                raise ValidationError("No Tasks in stage Done Found between selected dates")
        invoice_lines = []
        for task in done_tasks:
            invoice_lines.append((0, 0, {
                'name': task.task_name,
                'quantity': 1.0,
                'price_unit': sum(task.timesheet_ids.mapped('amount')),
            }))
            task.stage_id = self.env.ref('project_management.stage5_demo')
        move = self.env['account.move'].with_context({'default_project_id':self.project_id.id,
                                                      'default_task_ids':self.task_ids.ids}).create({
            'move_type': 'in_invoice',
            'partner_id': done_tasks[0].customer_id.id,
            'invoice_date': fields.Date.today(),
            'invoice_line_ids': invoice_lines,
        })
        move.write({
            'state': 'posted',
        })
        return move
        # return move,invoice_lines

    def generate_bill_print_report(self):
        created_move = self.generate_bill()
        return self.env.ref('project_management.action_report_bill').report_action(created_move)

    # def generate_bill_print_report1(self):
    #     created_move,data = self.generate_bill()
    #     return self.env.ref('project_management.action_report_bill_data').report_action(created_move,data=data)