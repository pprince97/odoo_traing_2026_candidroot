from odoo import api, fields, models

class BillWizard(models.TransientModel):
    _name = 'bill.wizard'
    _description = 'Bill Wizard'

    project_id = fields.Many2one('project.project_jui',string="project",ondelete='cascade')
    name=fields.Many2one('res.partner',related='project_id.customer_id',store=True)
    choice = fields.Selection([("task_wise", "Task wise"),('date_wise','Date wise')],string="Bill create by")
    task_ids=fields.Many2many('project.task_jui','task_bill_relation','bill_id','task_id',string="Task")
    start_date=fields.Date(string="Start Date")
    end_date=fields.Date(string="End Date")
    amount=fields.Float(string="Amount",compute='_compute_rate',store=True)
    amount_dict = dict()

    @api.onchange('start_date','end_date')
    def _onchange_date(self):
        if self.start_date and self.end_date:
            for rec in self:
                rec.task_ids = rec.task_ids.search([('done_date','>',rec.start_date),('done_date','<',rec.end_date),('stage_id.name','=','Done'),('project_id','=',rec.project_id.id)])

    @api.depends('task_ids')
    def _compute_rate(self):
        for rec in self:
            for task in rec.task_ids:
                rec.amount = 0
                end_ranges=[]
                start_ranges=[]
                for hr in  task.project_id.per_hour_rate_ids:
                    end_ranges.append(hr.end_range)
                    start_ranges.append(hr.start_range)
                    if hr.start_range < task.total_hours < hr.end_range:
                        rec.amount = task.total_hours * hr.per_hour_rate

                if rec.amount == 0:
                    for i in range(len(end_ranges)-1):
                        if end_ranges[i] < task.total_hours < start_ranges[i+1]:
                            rec.amount = task.total_hours * task.project_id.per_hour_rate_ids[i].per_hour_rate

                self.amount_dict[task] = rec.amount

    def wizard_create(self):
        res = self.env['account.move'].with_context({'default_move_type': 'in_invoice','default_project_id':self.project_id,'default_task_ids':self.task_ids}).create({'partner_id': self.name.id,'invoice_date':fields.Date.today()})
        for task in self.task_ids:
            self.env['account.move.line'].create({'move_id':res.id,'name':task.name,'price_unit':self.amount_dict[task]})
            task.stage_id = self.env.ref('project_management_jui.invoice_demo')
        res.update({'state':'posted'})

        return {
            'name': 'Bill',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_id' : res.id,
            'res_model': 'account.move',
            'target': 'self',
        }

    def wizard_create_print(self):
        res = self.env['account.move'].with_context({'default_move_type': 'in_invoice','default_project_id':self.project_id,'default_task_ids':self.task_ids}).create({'partner_id': self.name.id,'invoice_date':fields.Date.today()})
        for task in self.task_ids:
            self.env['account.move.line'].create({'move_id':res.id,'name':task.name,'price_unit':self.amount_dict[task]})
            task.stage_id = self.env.ref('project_management_jui.invoice_demo')
        res.update({'state':'posted'})

        data={
            'name' : res.name,
            'partner_id' : res.partner_id,
            'invoice_date' : res.invoice_date,
            'date' : res.date,
            'invoice_line_ids': [{'name': invoice.name, 'quantity': invoice.quantity,'price_unit': invoice.price_unit} for invoice in res.invoice_line_ids],
            'amount_residual' : res.amount_residual,
            'docs':res

        }
        print(data,'>>>>>>>>>>>>>>>>>>>>>>>>>>...')
        return self.env.ref('project_management_jui.action_report_bill').report_action(res.id)
        # return self.env.ref('project_management_jui.action_report_bill').report_action(res.id,data=data)
