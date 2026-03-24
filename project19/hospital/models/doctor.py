from odoo import fields,models,api

class Doctor(models.Model):
    _inherit='hr.employee'

    name=fields.Char('Name',required=True)
    age_d=fields.Char('Age')
    gender_d=fields.Selection([('male','Male'),('female','Female')],string='Gender')
    phone_d=fields.Integer('Phone no')
    email_d=fields.Char('Email')
    address_d=fields.Text('Address')
    department_d=fields.Char('Department')
    photo_d=fields.Image('photo')
    file_name_i= fields.Char(string='File Name')

    company_currency_id = fields.Many2one('res.currency', compute='_compute_company_currency_id')
    salary=fields.Monetary('Salary',currency_field='company_currency_id')
    is_available=fields.Boolean('Is_Available',default=True)

    patient=fields.One2many('patient.obj','doctor',string='Patient')
    app_id=fields.One2many('appointment.obj','d_id',string='Appointments')

    @api.depends_context('company')
    def _compute_company_currency_id(self):
        self.company_currency_id = self.env.company.currency_id
