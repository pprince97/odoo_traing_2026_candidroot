from odoo import models,fields,api

class Admission(models.Model):
    _name = 'hospital.admission'
    _description = 'Admission Model'

    name = fields.Char(string='Admission Name',required=True)
    patient_id = fields.Many2one(comodel_name='hospital.patient',string='Patient',ondelete='cascade')
    admit_date = fields.Datetime(string='Admit Date',readonly = True)
    discharge_date = fields.Datetime(string='Discharge Date',readonly = True)
    bed_no = fields.Char(string='Bed No')
    ward_type = fields.Selection([('general','General'),('semi','Semi'),('private','Private')],string='Ward Type',default='general')
    bill_amount = fields.Float(string='Bill Amount')
    paid_amount = fields.Float(string='Paid Amount')
    notes = fields.Text(string='Notes')
    is_active = fields.Boolean(string='Active',readonly = True)

    def admit_patient(self):
        self.admit_date = fields.Datetime.now()
        self.is_active = True

    def discharge_patient(self):
        self.discharge_date = fields.Datetime.now()
        self.is_active = False

    def mark_paid(self):
        self.paid_amount = self.bill_amount