# ● Hospital
# ● Patient (only patients should appear)
# ● Department
# ● Doctor (filtered based on selected department and hospital)
# ● Appointment Date (default today, cannot be in the past)
# ● Patient Address (auto-filled)
# ● Patient Date of Birth (auto-filled)
# ● Patient age, Mobile, Email (auto-filled)
# ● Status (New, In Progress, Done, Cancelled)
# Smart Button:
# ● Appointments
# ■ Shows only appointments related to that doctor, patient and hospital.

from odoo import fields,models,api
from odoo.exceptions import ValidationError
from datetime import datetime,date

class AppointmentModel(models.Model):
    _name='appointment.model'
    _description='Appointment'
    _rec_name='patient_id'

    hospital_id=fields.Many2one('hospital.model',string='Hospital',required=True)
    patient_id=fields.Many2one('res.partner',string='Patient',required=True,domain=[('patient_code','ilike','p%')],context={'is_patient':True})

    department_id=fields.Many2one('department.model',string='Department',ondelete='cascade')
    doctor_id=fields.Many2one('res.partner',string='Doctor',required=True,domain=[('doctor_code','ilike','d%')],context={'is_doctor':True})

    appointment_date=fields.Date(string='Appointment Date',default=datetime.today())
    patient_address=fields.Char(string='Patient Address',related='patient_id.city',store=True)
    patient_dob=fields.Date(string='Date of Birth',related='patient_id.date_of_birth',store=True)
    patient_age=fields.Char(string='Age',related='patient_id.age',store=True)
    patient_mobile=fields.Char(string='Mobile',related='patient_id.phone',store=True)
    patient_email=fields.Char(string='Email',related='patient_id.email',store=True)

    status=fields.Selection([('new','New'),('in_progress','In Progress'),('done','Done'),('cancelled','Cancelled')],string='Status',default='new')

    @api.onchange('doctor_id')
    def _onchange_patient(self):
        for rec in self:
            if not rec.department_id:
                rec.department_id=rec.doctor_id.department_id

    @api.onchange('appointment_date')
    def _onchange_appointment_date(self):
        for rec in self:
            new = str(rec.appointment_date)
            l = new.split('-')
            s = str(datetime.today()).split()[0].split('-')
            start_date = date(int(l[0]), int(l[1]), int(l[2]))
            end_date = date(int(s[0]), int(s[1]), int(s[2]))
            diff = end_date - start_date
            if diff.days > 0:
                self.appointment_date=datetime.today()
                print(self.appointment_date)
                raise ValidationError("Date cannot be in past")


    def appointment_a_btn(self):
        return {
            'name': "Appointment",
            'type': 'ir.actions.act_window',
            'view_mode': 'list,form',
            'res_model': 'appointment.model',
            'target': 'self',
            'domain': [
                ("patient_id", "=", "patient_id"),
            ],
        }

    def in_progress_status(self):
        appointment=self.env['appointment.model'].search([('patient_id','=',self.patient_id.id),('status','=','in_progress')])
        if appointment:
            raise ValidationError("Only one appointment can be in In Progress state at a time")
        else:
            self.update({'status':'in_progress'})
    def done_status(self):
        self.update({'status':'done'})
    def cancel_status(self):
        print("\n Cancelled field >>>>>> ", self.read())
        self.update({'status':'cancelled','appointment_date':False})
