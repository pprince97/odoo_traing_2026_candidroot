from odoo import models,fields,api

class Appointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Appointment Model'

    name = fields.Char(string='Name')
    patient_id = fields.Many2one(comodel_name='hospital.patient',string='Patient',ondelete='cascade')
    doctor_id = fields.Many2one(comodel_name='hospital.doctor',string='Doctor')
    appointment_date = fields.Datetime(string='Appointment Date',readonly=True)
    status = fields.Selection([('draft', 'Draft'),('confirm', 'Confirm'),('done', 'Done'),('cancel', 'Cancel')],string='Status',default='draft')
    token_no = fields.Char(string='Token No')
    fees = fields.Float(string='Fees', compute='_compute_fees', inverse='_inverse_fees', store=True)
    paid = fields.Float(string='Paid')
    description = fields.Text(string='Description')
    prescription = fields.Html(string='Prescription')
    attachment = fields.Binary(string='Attachment')
    followup_date = fields.Datetime(string='Followup Date')
    duration_minutes = fields.Integer(string='Duration Minutes')
    is_emergency = fields.Boolean(string='Emergency')
    currency_id_m = fields.Many2one('res.currency')
    ap_fees = fields.Monetary(currency_field='currency_id_m',string='Appointment Fees')

    @api.depends('status')
    def _compute_fees(self):
        # print('>>>>>>>>>>>>>>>>>>>>Compute')
        for rec in self:
            print("\n\n ccccccccccccccccccc")
            if rec.status in ['confirm']:
                rec.fees = 500
            else:
                rec.fees = 0
    def _inverse_fees(self):
        for rec in self:
            rec.fees = rec.fees
        # print("\n\n ccccccccccccccccccc")
        # if rec.fees > 0:
        # else:
        #     rec.fees = 0

    def write(self, vals):
        res = super(Appointment, self).write(vals)
        return res

    def confirm_status(self):
        self.write({'appointment_date': fields.Datetime.now()})
        self.write({'status': "confirm"})

    def cancel_status(self):
        rec = self.env['hospital.appointment'].browse(self.id)
        print('canceling appointment:',rec.name)
        rec.unlink()
        self.write({'appointment_date': None})
        self.write({'status': "cancel"})

    def done_status(self):
        self.write({'status': "done"})

    def server_action_method(self):
            self.description = 'Change from server action'

    def server_action_method1(self):
            self.description = 'Change from server action1'

    @api.depends_context('company')
    def _compute_company_currency_id(self):
        self.company_currency_id = self.env.company.currency_id




