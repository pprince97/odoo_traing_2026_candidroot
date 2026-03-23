from odoo import models,fields,api

class Appointment(models.Model):
    _name = "hospital.appointment"
    _description = "Appointment"

    app_datetime = fields.Datetime("Appointment Date time")
    doctor_id = fields.Many2one("hospital.doctor",ondelete="restrict",string="Doctor")
    patient_id = fields.Many2one("hospital.patient", ondelete="restrict", string="Patient")
