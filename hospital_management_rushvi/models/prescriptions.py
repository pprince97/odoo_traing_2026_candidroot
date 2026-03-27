from odoo import models,fields,api
from odoo.exceptions import ValidationError


class Hospitals(models.Model):
    _name = 'hospital.management.prescriptions'
    _description = 'Prescriptions'
    _rec_name = 'patient_id'

    medicine = fields.Char("Medicine")
    quantity = fields.Integer("Quantity")
    frequency = fields.Char("Frequency")
    patient_id = fields.Many2one('res.partner',string="Patient")
