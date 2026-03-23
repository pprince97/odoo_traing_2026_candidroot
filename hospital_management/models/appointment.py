from odoo import models, fields, api

class Appointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Appointment'

    name = fields.Char(string='Name')
    app_date = fields.Date(string='Appointment Date', readonly=True)
    status = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'), ('done', 'Done'), ('cancel', 'Cancel')],
                              string='Status', default='draft')
    token_no = fields.Char(string='Token Number')
    fees = fields.Float(string='Fees', readonly=False, default=1.2)
    paid = fields.Float(string='Paid Amount')
    description = fields.Text(string='Description')
    prescription = fields.Html(string='Prescription')
    attachment = fields.Binary(string='Attachment')
    followup_date = fields.Date(string='Followup Date')
    duration_minute = fields.Integer(string='Duration in minutes')
    is_emergency = fields.Boolean(string='Is Emergency ?', default=True)
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor')
    patient_id = fields.Many2one('hospital.patient', ondelete='cascade', required=True)
    # currency_id = fields.Many2one('res.currency', compute='_compute_company_currency_id')
    # fees_monetary = fields.Monetary(string='Fees Monetary', currency_field='currency_id')


    def confirm_appointment(self):
        self.write({'status': 'confirm', 'app_date': fields.Date.today()})

    def mark_done(self):
        self.write({'status': 'done', 'app_date': fields.Date.today()})

    def cancel(self):
        self.write({'status': 'cancel', 'app_date': None})

    def draft(self):
        self.write({'status': 'draft', 'app_date': fields.Date.today()})

    # @api.depends_context('company')
    # def _compute_company_currency_id(self):
    #     self.company.currency_id = self.env.company.currency_id
