from odoo import api, fields, models

class ProjectBillingWizard(models.TransientModel):
    _name = "wizard.create_project_bill"
    _description = "Project Billing Wizard"

    select = fields.Selection([
        ('task_wise','Task wise'),
        ('date_wise','Date wise'),
    ],default="task_wise")
    project_id = fields.Many2one('project.projects', string="Project")
    task_ids = fields.One2many(related='project_id.task_ids', string="Tasks")
    start_date = fields.Datetime(string="Start Date")
    end_date = fields.Datetime(string="End Date")
    selected_task_ids = fields.Many2many('project.tasks', 'task_project_bill_rel' , 'task_id' , 'project_bill_id', string="Selected Tasks",
                                         domain="[('id', 'in', task_ids),('stage_id.name', '=', 'Done')]")
    account_id = fields.Many2one('account.move', string="Account")


    def generate_project_bill(self):
        # self.env['project.projects'].invoice_state()
        self.project_id.update({'state': 'invoice'})

        paid_state = self.env.ref('project_management_sankit.demo_stage_paid')
        print("--------====  ", paid_state)
        self.selected_task_ids.write({'stage_id': paid_state})

        self.ensure_one()
        l = []
        for i in self.selected_task_ids:
            print('i.name>>>>>>>>>>.', i.name)
            l.append((0, 0, {'name': i.name, 'quantity': 1, 'price_unit': i.total_amount}))
            print(l)
        res = self.env['account.move'].with_context({'default_move_type': 'in_invoice'}).create(
            {'partner_id': self.project_id.customer_id.id, 'invoice_date': fields.Date.today(), 'invoice_line_ids': l})

        return {
            'name': self.project_id.customer_id.name,
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': res.id,
            'target': 'new'
        }

    def generate_project_pdf(self):
        self.project_id.update({'state': 'invoice'})
        self.ensure_one()
        generate_bill = self.generate_project_bill()
        return self.env.ref('account.account_invoices').report_action(generate_bill['res_id'])

    # def _get_report_data(self):
    #     l = []
    #     for i in self.selected_task_ids:
    #         print('i.name>>>>>>>>>>.', i.name)
    #         l.append((0, 0, {'name': i.name, 'quantity': 1, 'price_unit': i.total_amount}))
    #         print(l)
    #     return {'partner_id': self.project_id.customer_id.id, 'invoice_date': fields.Date.today(), 'invoice_line_ids': l}

    def generate_project_bill_using_dics(self):
        self.ensure_one()
        l = []
        for i in self.selected_task_ids:
            print('i.name>>>>>>>>>>.', i.name)
            l.append((0, 0, {'name': i.name, 'quantity': 1, 'price_unit': i.total_amount}))
            print(l)
        data = {'partner_id': self.project_id.customer_id.id,
                'invoice_date': fields.Date.today(),
                'invoice_line_ids': l
                }
        return self.env.ref('account.account_invoices').report_action([self.account_id.id],data=data)

    # def _get_report_data(self):
    #     return {'date_start': False, 'date_stop': False, 'config_ids': self.pos_session_id.config_id.ids, 'session_ids': self.pos_session_id.ids}
    #
    # def generate_report(self):
    #     return self.env.ref('point_of_sale.sale_details_report').report_action([], data=self._get_report_data())

    def generate_project_bill_using_date(self):
        self.project_id.update({'state': 'invoice'})
        l = []
        print('in outer >>>>>>>>>>', self.selected_task_ids)
        for i in self.task_ids:
            print('in for >>>>>>>>>>.', i.name)
            if i.start_date >= self.start_date:
                print('in if >>>>>>>>>>.', i.name)
                if i.end_date <= self.end_date:
                    print('i.name>>>>>>>>>>.', i.name)
                    l.append((0, 0, {'name': i.name, 'quantity': 1, 'price_unit': i.total_amount}))

        res = self.env['account.move'].with_context({'default_move_type': 'in_invoice'}).create(
            {'partner_id': self.project_id.customer_id.id, 'invoice_date': fields.Date.today(), 'invoice_line_ids': l})

        return {
            'name': self.project_id.customer_id.name,
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': res.id,
            'target': self
        }







