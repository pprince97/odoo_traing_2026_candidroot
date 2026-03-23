from odoo import models,fields,api

class Bill(models.Model):
    _inherit = "account.move"

    hospital_id = fields.Many2one('hospital.hospital',string='Hospital',ondelete='cascade')
    doctor_id = fields.Many2one('hospital.doctor',string="Doctor",ondelete='cascade')
    patient_id = fields.Many2one('hospital.patient',string="Patient",ondelete='cascade')