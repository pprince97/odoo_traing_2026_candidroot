from odoo import fields, api, models
from datetime import date, datetime
from odoo.exceptions import ValidationError


class Appointment(models.Model):
    _name = 'appointments.object'
    _description = 'Hospital Appointment'
    _rec_name = 'hospital_id'

    hospital_id = fields.Many2one('hospital.object', string='Hospital')
    patient_id = fields.Many2one('res.partner', string='Patient', domain=[('patient_code', 'ilike', 'P%')])

    doctor_id = fields.Many2one('res.partner', string='Doctor')

    department_id = fields.Many2one('department.object', string='Department')

    appointment_date = fields.Date(string='Appointment Date')
    patient_address = fields.Char(string='Patient Address', readonly=True)
    patient_dob = fields.Datetime(string='Patient DOB', readonly=True)
    patient_age = fields.Char(string='Patient Age', readonly=True, store=True)
    patient_mobile = fields.Char(string='Patient Mobile', readonly=True)
    patient_email = fields.Char(string='Patient Email', readonly=True)

    state = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ],
        default='new',
        string='State',
    )



    def action_in_progress(self):
        self.update({'state': 'in_progress'})

    def action_done(self):
        self.update({'state': 'done'})
        print("\n\nDoctor ===============> ", self.doctor_id)

    def action_new(self):
        self.update({'state': 'new'})

    # @api.model_create_multi
    # def create(self, vals_list):
    #     today_date = date.today()
    #
    #     if vals_list["appointment_date"]:
    #         formate = "%Y-%m-%d %I:%M:%S"
    #         date_object = datetime.strptime(vals_list["appointment_date"], formate).date()
    #         if date_object < today_date:
    #             raise ValidationError("Date cannot be in the past.")
    #
    #     res = super().create(vals_list)
    #     return res


    @api.onchange('patient_id')
    def onchange_patient_id(self):
        self.patient_age = self.patient_id.p_age
        self.patient_mobile = self.patient_id.phone
        self.patient_email = self.patient_id.email
        self.patient_dob = self.patient_id.p_date_of_birth
        self.patient_address = self.patient_id.p_address

    # @api.depends('patient_id')
    # def _compute_patient_age(self):
    #     self.patient_age = self.patient_id.p_age
    #     self.patient_mobile = self.patient_id.phone
    #     self.patient_email = self.patient_id.email
    #     self.patient_dob = self.patient_id.p_date_of_birth
    #     self.patient_address = self.patient_id.p_address


    related_appointment_count = fields.Integer(compute='get_appointment_related_data')

    def get_appointment_related_data(self):
        self.ensure_one()

        self.related_appointment_count = self.env['appointments.object'].search_count([
            ('patient_id', '=', self.patient_id.id),
            ('doctor_id', '=', self.doctor_id.id),
            ('hospital_id', '=', self.hospital_id.id),
        ])

        return {
            'type':'ir.actions.act_window',
            'res_model': 'appointments.object',
            'name': 'Appointment Related Data',
            'view_mode': 'list,form',
            'domain': [
                ('patient_id', '=', self.patient_id.id),
                ('doctor_id', '=', self.doctor_id.id),
                ('hospital_id', 'in', self.hospital_id.id),
            ]
        }