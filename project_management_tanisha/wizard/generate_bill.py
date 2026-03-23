from odoo import models,fields,api,_

class Bill(models.TransientModel):
    _name = 'project.bill.wizard'
    _description = 'Bill Wizard'

    choice = fields.Selection([('datewise','Datewise'),('taskwise','Taskwise')],string='Billing Choice',default='datewise')
    start_date = fields.Datetime(string='Start Date')
    end_date = fields.Datetime(string='End Date')
    task_ids = fields.Many2many('project.tanisha.task','task_bill_rel','bill_id','task_id',string='Tasks')
    project_id = fields.Many2one('project.tanisha.project',string='Project')

    def generate_bill(self):
        l = []
        stage_invoice = self.env['project.stage'].search([('name', '=', 'Invoice')])
        if self.choice == 'taskwise':
            tasks = self.env['project.tanisha.task'].search([('project_id', '=', self.project_id.id), ('id', 'in', self.task_ids.ids)])
            for task in tasks:
                l.append((0, 0, {
                    'name': task.name,
                    'quantity': task.total_hours,
                    'price_unit': task.rate,
                    'price_subtotal': task.rate*task.total_hours,
                }))
                task.stage_id = stage_invoice.id
        else:
            if self.start_date and self.end_date:
                tasks = self.env['project.tanisha.task'].search([('project_id', '=', self.project_id.id)])
                for task in tasks:
                    if (task.start_date>=self.start_date) and (task.end_date<=self.end_date):
                        l.append((0, 0, {
                            'name': task.name,
                            'quantity': task.total_hours,
                            'price_unit': task.rate,
                            'price_subtotal': task.rate*task.total_hours,
                        }))
                    task.stage_id = stage_invoice.id

        create_bill = self.env['account.move'].with_context(default_move_type='in_invoice',default_project_id=self.project_id,default_task_ids=self.task_ids).create({
            'partner_id': self.project_id.customer_id.id,
            'invoice_date': fields.Date.today(),
            'invoice_line_ids': l,
        })
        for rec in create_bill:
            rec.project_id.show_bills()
            rec.task_ids.show_bills()
        return {
            'type': 'ir.actions.act_window',
            'target': 'self',
            'res_model': 'account.move',
            'res_id': create_bill.id,
            'view_mode': 'form',
        }

    def generate_bill_and_report(self):
        a = self.generate_bill()
        return self.env.ref('project_management_tanisha.generate_bill_report').report_action(a['res_id'], config=False)