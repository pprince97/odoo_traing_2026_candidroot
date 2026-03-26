# (Inherit res.partner)
# Details:
# ● Auto-generated Patient ID (P0001, P0002, etc.)
# ● Name
# ● Date of Birth
# ● Age (auto-calculated in years, months, and days)
# ● Address
# ● Mobile
# ● Email
# Smart Button:
# ● Appointments
# ■ Shows only appointments related to that patient.
# ■ When creating a new appointment from here, the patient is selected
# automatically.
from dateutil.relativedelta import relativedelta
from odoo import fields, models, api,Command
from datetime import datetime,date


class PatientModel(models.Model):
    _inherit = 'res.partner'
    _rec_name = 'patient_code'

    patient_code = fields.Char(string='Patient Id',readonly=True)
    date_of_birth = fields.Date(string='Date of Birth', required=True, default=fields.Date.today())
    age = fields.Char(string='Age', compute='_compute_age', store=True)

    hospital_ids=fields.Many2many('hospital.model','hospital_patient_relation','patient_id','hospital_id',string='Hospitals')

    appointment_count=fields.Integer(string='Appointment Count')

    @api.model_create_multi
    def create(self, vals):
        if self.env.context.get('is_patient'):
            for rec in vals:
                rec['patient_code'] = self.env['ir.sequence'].next_by_code('patient.seq')
        res = super(PatientModel, self).create(vals)
        for rec in res:
            if rec and self.env.context.get('is_patient'):
                user = self.env['res.users']
                user.create(
                    {'name': rec.name, 'login': rec.name, 'email': rec.email, 'partner_id': rec.id, 'password': 'admin',
                     'group_ids': [Command.set([self.env.ref('hospital_management.hospital_group_patient').id])]})
        return res

    def appointment_p_btn(self):
        self.appointment_count = self.env['appointment.model'].search_count([
            ("patient_id", "=", self.id),
        ])

        d = {
                'name': "Appointment",
                'type': 'ir.actions.act_window',
                'view_mode': 'list,form',
                'res_model': 'appointment.model',
                'target': 'self',
                'domain': [
                    ("patient_id", "=", self.id),
                ],
                'context':{'default_patient_id':self.id}
            }

        if self.appointment_count == 1:
            d['view_mode']= 'form'
            d['res_id'] = self.env['appointment.model'].search([
                ("patient_id", "=", self.id),
            ]).id
        return d

    @api.depends('date_of_birth')
    def _compute_age(self):
        for rec in self:
            if rec.date_of_birth:
                new = str(rec.date_of_birth)
                l = new.split('-')
                s = str(datetime.now()).split()[0].split('-')
                start_date = date(int(l[0]), int(l[1]), int(l[2]))
                end_date = date(int(s[0]), int(s[1]), int(s[2]))
                diff = relativedelta(end_date,start_date)
                rec.age= f'{diff.years} years {diff.months} months {diff.days} days old'

# 2026-02-03
