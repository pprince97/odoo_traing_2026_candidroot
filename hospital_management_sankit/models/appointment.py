from datetime import datetime
from datetime import date

from random import randint
import random
from odoo import fields, api, models

from odoo.exceptions import ValidationError


class Appointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Hospital Appointment'


    hospital_id = fields.Many2one('hospital.hospital', string='Hospital')
    patient_id = fields.Many2one('res.partner', string='Patient', required=True,
                                 domain="([('patient_code', 'ilike', 'P/%')])")
    department_id = fields.Many2one('hospital.department', string='Department')
    doctor_id = fields.Many2one('res.partner',
                                string='Doctor')
    # domain = "([('hospital_id', '=', hospital_id),('department_id', '=', department_id)])"

    today_date = fields.Datetime.now()
    appointment_date = fields.Date(string="Appointment Date")
    patient_address = fields.Char(string="Patient Address", readonly=True)
    patient_dob = fields.Date(string="Patient DOB", readonly=True)
    patient_age = fields.Integer(string="Patient Age", readonly=True, compute="_compute_patient_age", store=True)
    patient_phone = fields.Char(string="Patient Phone", readonly=True)
    patient_email = fields.Char(string="Patient Email", readonly=True)

    appointment_count = fields.Integer(string='Appointment Count')

    status = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('in_progress', 'In Progress'),
            ('done', 'Done'),
            ('cancel', 'Cancel'),
        ],
        default='draft',
        string="status", )

    def draft_state(self):
        current_in_progress = self.env['hospital.appointment'].search([('status', '=', 'in_progress')])
        if not current_in_progress:
            self.update({'status': "in_progress"})
        else:
            raise ValidationError("Only 1 appointment at a time in progress")

    def in_progress_state(self):

        self.update({'status': "done"})

    def done_state(self):
        self.update({'status': "draft"})

    @api.model_create_multi
    def create(self, vals_lists):
        for vals_list in vals_lists:
            today_date = date.today()
            if vals_list.get('appointment_date'):
                formate = "%Y-%m-%d %I:%M:%S"
                date_object = datetime.strptime(vals_list["appointment_date"], formate).date()
                if date_object < today_date:
                    raise ValidationError("Date is Not In Past")

            # appointment = self.env['res.partner'].search([('appointment_ids', '=', self.id)])
            # print(appointment,":::::::::::::::")
            # self.write({'patient_address': appointment.address})
            # self.patient_dob = self.env['res.partner']._fields.get('dob')

        res = super().create(vals_lists)
        return res

    def action_hospital_record(self):
        self.ensure_one()

        self.appointment_count = self.env['hospital.appointment'].search_count(
            [('patient_id', '=', self.patient_id.id),
             ('doctor_id', '=', self.doctor_id.id),
             ('hospital_id', '=', self.hospital_id.id),
             ])
        print(self.appointment_count, "++++++++++++")
        # print(len(appointment),"***********")
        return {
            'name': "Appointment",
            'type': 'ir.actions.act_window',
            'res_model': 'hospital.appointment',
            'view_mode': 'list,form',
            'domain': [('patient_id', '=', self.patient_id.id),
                       ('doctor_id', '=', self.doctor_id.id),
                       ('hospital_id', '=', self.hospital_id.id)
                       ],
            'target': 'current',
        }

    @api.onchange('patient_id')
    def _onchange_patient(self):
        self.patient_address = self.patient_id.address
        self.patient_email = self.patient_id.email
        self.patient_age = self.patient_id.age_year
        self.patient_phone = self.patient_id.phone
        self.patient_dob = self.patient_id.dob

    @api.depends('patient_id')
    def _compute_patient_age(self):
        self.patient_age = self.patient_id.age_year
        self.patient_address = self.patient_id.address
        self.patient_email = self.patient_id.email

        self.patient_phone = self.patient_id.phone
        self.patient_dob = self.patient_id.dob
