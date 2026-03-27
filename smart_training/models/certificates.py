from odoo import models,fields,api

class SmartTrainingCertificates(models.Model):
    _name = "smart.training.certificates"
    _description = "Smart Training Certificates"

    name = fields.Char(string="Name")
    employee_id = fields.Many2one('hr.employee',string="Employee")
    session_id = fields.Many2one('smart.training.sessions',string="Session")
    program_id = fields.Many2one('smart.training.programs',string="Program")
    issue_date = fields.Datetime(string="Issue Date", default=fields.Datetime.now())
    score = fields.Float(string="Final Score")
    status = fields.Selection([('draft', 'Draft'), ('issued', 'Issued')],
                                   string="Level",default='draft',required=True)
    certificate_file = fields.Binary(string="Certificate File")
    certificate_file_name = fields.Char(string="Certificate File Name")
    notes = fields.Text(string="Feedback")

    def issued_status(self):
        self.status = 'issued'

    @api.model_create_multi
    def create(self, vals_list):
        res = super(SmartTrainingCertificates, self).create(vals_list)
        for rec in res:
            rec.name = f"CFT - {rec.id:05d}"
        return res