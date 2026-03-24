# (Inherit res.partner)
# Details:
# ● Auto-generated Doctor ID (D0001, D0002, etc.)
# ● Name
# ● Address
# ● Mobile
# ● Email
# ● Department
# ● Experience
# ● Specialty / Description
# ● Related Hospitals
# Smart Button:
# ● Appointments
# ■ Shows only appointments related to that doctor.
# ■ When creating a new appointment from here, the doctor is selected
# automatically.

from odoo import fields,models,api,Command
from odoo.fields import Domain

class DoctorModel(models.Model):
    _inherit='res.partner'
    _rec_name = 'doctor_code'

    doctor_code=fields.Char(string='Doctor ID', readonly=True)
    department_id=fields.Many2one('department.model',string='Available Department',ondelete='cascade')
    experience=fields.Integer(string='Experience')
    description=fields.Text(string='Speciality/Description')

    hospital_id=fields.Many2many('hospital.model','hospital_doctor_relation','doctor_id','hospital_id',string='Hospital')
    appointment_count=fields.Integer(string='Appointment Count')

    @api.model_create_multi
    def create(self, vals):
        if self.env.context.get('is_doctor'):
            for rec in vals:
                rec['doctor_code'] = self.env['ir.sequence'].next_by_code('doctor.seq') or 'New'

        res = super(DoctorModel, self).create(vals)
        for rec in res:
            if rec and self.env.context.get('is_doctor'):
                user = self.env['res.users']
                user.create({'name':rec.name,'login': rec.name,'email':rec.email,'partner_id':rec.id,'password': 'admin','group_ids':[Command.set([self.env.ref('hospital_management.hospital_group_doctor').id])]})
        return res


    def appointment_d_btn(self):
        self.appointment_count = self.env['appointment.model'].search_count([
            ("doctor_id", "=", self.id),
        ])

        d = {
                'name': "Appointment",
                'type': 'ir.actions.act_window',
                'view_mode': 'list,form',
                'res_model': 'appointment.model',
                'target': 'self',
                'domain': [
                    ("doctor_id", "=", self.id),
                ],
                'context': {'default_doctor_id': self.id}
            }

        if self.appointment_count == 1:
            d['view_mode']='form'
            d['res_id'] = self.env['appointment.model'].search([
                ("doctor_id", "=", self.id),
            ]).id
        return d

    @api.model
    @api.readonly
    def name_search(self, name='', domain=None, operator='ilike', limit=100):
        if self.env.context.get("doctor_appointment"):
            d = self.env.context.get("department")
            h = self.env.context.get("hospital")
            domain = Domain('doctor_id', 'like', 'D%')
            if d and h:
                domain &= Domain('department_id', '=', d)
                domain &= Domain('hospital_ids.id', '=', h)
            elif d:
                domain &= Domain('department_id', '=', d)
            elif h:
                domain &= Domain('hospital_ids.id', '=', h)
                print(domain)
            records = self.search(domain)
            return [(record.id, record.display_name) for record in records]
        return super().name_search(name, domain, operator, limit)