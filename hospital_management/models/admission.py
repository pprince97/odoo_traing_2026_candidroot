from odoo import models, fields, api


class Admission(models.Model):
    _name = 'hospital.admission'
    _description = 'Admission'

    name = fields.Char(string='Name')
    admit_date = fields.Date(string='Admit Date')
    discharge_date = fields.Date(string='Discharge Date')
    bed_no = fields.Integer(string='Bed no')
    ward_type = fields.Selection([('general', 'General'), ('semi', 'Semi'), ('private', 'Private')], string='Selection',
                                 default='general')
    bill_amount = fields.Float(string='Bill Amount')
    paid_amount = fields.Float(string='Paid Amount')
    notes = fields.Text(string='Notes')
    is_active = fields.Boolean(string='Is Active', default=True)
    patient_id = fields.Many2one('hospital.patient', ondelete='cascade', string='Patient')
    adm_name = fields.Char(related='patient_id.name', string='Patient Name from object', store=True)


    def admit(self):
        self.admit_date = fields.Date.today()
        self.is_active = True

    def discharge(self):
        self.discharge_date = fields.Date.today()
        self.is_active = False

    def mark_paid(self):
        self.paid_amount = self.bill_amount
