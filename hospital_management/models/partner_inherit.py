from odoo import models, fields, api

class PartnerInherit(models.Model):
    _inherit = 'res.partner'

    is_patient = fields.Boolean(string='Is Patient ?')
    is_doctor = fields.Boolean(string='Is Doctor ?')
    patient_code = fields.Char(string='Patient Code', readonly=True)
    blood_grp = fields.Selection(
        [('a+', 'A+'), ('b+', 'B+'), ('ab+', 'AB+'), ('o+', 'O+'), ('a-', 'A-'), ('b-', 'B-'), ('ab-', 'AB-'),
         ('o-', 'O-')], default='a+')
    height = fields.Float(string='Height (cm)')
    weight = fields.Float(string='Weight (kg)')
    med_history = fields.Text(string='Medical History')
    ins_doc = fields.Binary(string='Insurance Document')
    ins_filename = fields.Char(string='Insurance File Name')
    last_visit_date = fields.Date(string='Last Visit Date')
    next_visit_datetime = fields.Datetime(string='Next Visit Datetime')
    emer_conid = fields.Char(string='Emergency Contact ID')
    risk_level = fields.Selection([('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], string='Risk level',
                                  default='low')
    patient_ids = fields.One2many('hospital.patient', 'partner_id', string='Patients')

    def gen_patient_code(self):
        if len(str(self.id)) == 1:
            self.patient_code = '00' + str(self.id)
        elif len(str(self.id)) == 2:
            self.patient_code = '0' + str(self.id)
        else:
            self.patient_code = str(self.id)


