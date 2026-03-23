from odoo import models,fields,api

class Appointment(models.Model):
        _name = "hospital.appointment"
        _description = "Appointment Model"
        _rec_name = "appointment_datetime"

        patient_id = fields.Many2one('hospital.patient',string="Patient",ondelete="cascade")
        appointment_datetime = fields.Datetime("Appointment Datetime")
        appointment_status = fields.Selection([("book",'Book'),('in_process','In Process'),('confirm','Confirm')],string="Appointment Status",default="book")
        doctor_id = fields.Many2one("hospital.doctor",string="Doctor",ondelete="cascade")
        department_id = fields.Many2one('hr.department',string="Department",ondelete="cascade")
        hospital_ids = fields.Many2many('hospital.hospital', 'hos_app_rel', 'appointment_id','hospital_id',
                                           string="Hospitals")

        def status_book(self):
                self.write({'status': "in_process"})

        def status_in_process(self):
                # Student = self.env['school.student']
                # Student.create(
                #         {'name': self.student_name, 'email': self.email, 'percentage': self.percentage,
                #          'gender': self.gender,
                #          'date_of_birth': self.dob,
                #          'admission_datetime': self.admission_date, 'id_proof': self.id_proof,
                #          'file_name': self.file_name,
                #          'photo': self.photo, 'school_id': self.school_id.id})
                self.write({'stage': "confirm"})

        def status_confirm(self):
                self.write({'stage': "Book"})
