from odoo import fields,models,api

class Bill(models.Model):
    _inherit='account.move'

    patient_id=fields.Many2one('patient.obj',string='Patient',ondelete='cascade')
    # d_id=fields.Char(string='Doctor',related='patient_id.doctor',store=True)
    insurance_no=fields.Char('Insurance reference number')

