from odoo import models,fields,api
from datetime import datetime

class AdmissionModel(models.Model):
    _name='admission.model'
    _description='Admission Model'

    name=fields.Char(string='Name')
    patient_id=fields.Many2one('patient.model',string='Patient',ondelete='cascade')
    admit_date=fields.Datetime(string='Admission Date',readonly=True)
    discharge_date=fields.Datetime(string='Discharge Date',readonly=True)
    bed_no=fields.Char(string='Bed No')
    ward_type=fields.Selection([('general','General'),('semi','Semi'),('private','Private')],string='Ward')
    bill_amount=fields.Float(string='Bill Amount')
    paid_amount=fields.Float(string='Paid Amount',readonly=True)
    notes=fields.Text(string='Notes')
    p_active=fields.Boolean(string='Active')

    def admit_p(self):
        self.update({'p_active':True,'admit_date':datetime.now()})
        patient = self.env['patient.model'].search([('name','=',self.patient_id.name)])
        patient.update({'active_p': True})
        print(self.patient_id.name)
        print(patient.name)
    def discharge_p(self):
        self.update({'p_active':False,'discharge_date':datetime.now()})
        patient = self.env['patient.model'].search([('name', '=', self.patient_id.name)])
        patient.update({'active_p': False})
    def mark_paid(self):
        self.update({'paid_amount':self.bill_amount})