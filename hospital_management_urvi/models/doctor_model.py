from odoo import models, fields, api, Command
from odoo.fields import Domain


class Doctor(models.Model):
    _inherit = "res.partner"

    doctor_id = fields.Char(string="Doctor ID", readonly=True)  # auto generate
    # name  = from res.partner
    # address  = from res.partner
    # mobile  = from res.partner
    # email  = from res.partner
    department_id = fields.Many2one('hospital.department', string="Department", ondelete='restrict')
    experience = fields.Float(string="Experience", help="Enter experience in years")
    # Specialty / Description = from res.partner
    hospital_ids = fields.Many2many('hospital.hospital', 'hospital_doctor_rel', 'doctor_id', 'hospital_id',
                                    string='Hospital')
    member = fields.Selection([('doctor', 'Doctor'), ('patient', 'Patient')], string="Member")
    da_counts = fields.Integer(string="Appointment Count's", compute='_compute_da_count')

    @api.model_create_multi
    def create(self, vals):
        if self.env.context.get("doctor"):
            for val in vals:
                if val.get('doctor_id', 'New') == 'New':
                    val['doctor_id'] = self.env['ir.sequence'].next_by_code('doctor.sequence') or 'New'
        res = super(Doctor, self).create(vals)
        if self.env.context.get("doctor"):
            for rec in res:
                # if rec.member=='doctor':
                #         d_id = self.env['res.partner'].search_count([('member', '=', 'doctor')])
                #         if d_id < 10:
                #             rec.doctor_id = 'D000' + str(d_id)
                #         elif d_id < 100:
                #             rec.doctor_id = 'D00' + str(d_id)
                #         elif d_id < 1000:
                #             rec.doctor_id = 'D0' + str(d_id)
                #         else:
                #             rec.doctor_id = 'D' + str(d_id)
                if rec:
                    self.env['res.users'].create(
                        {'name': rec.name,
                         'email': rec.email,
                         'partner_id': rec.id,
                         'login': rec.name,
                         'password': rec.name,
                         'signature': rec.name,
                         'group_ids': [Command.set([self.env.ref('hospital_management_urvi.group_hospital_doctor').id])]})
        return res

    def _compute_da_count(self):
        self.da_counts = self.env['hospital.appointment'].search_count([('doctor_id', '=', self.id)])

    def view_appointment_doctor(self):
        rd = {
            'name': self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'hospital.appointment',
            'view_mode': 'list,form',
            'domain': [('doctor_id', '=', self.id)],
            'context': {'default_doctor_id': self.id},
            'target': self
        }
        if self.da_counts == 1:
            rd['view_mode'] = 'form'
            rd['res_id'] = self.env['hospital.appointment'].search(
                [('doctor_id', '=', self.id)]).id
        return rd

    @api.model
    @api.readonly
    def name_search(self, name='', domain=None, operator='ilike', limit=100):
        if self.env.context.get("doctor"):
            a = self.env.context.get("ap")
            h = self.env.context.get("hos")
            domain = Domain('doctor_id', 'like', 'D%')
            if a and h:
                domain &= Domain('department_id', '=', a)
                domain &= Domain('hospital_ids.id', '=', h)
                print(domain)
                records = self.search(domain)
                return [(record.id, record.display_name) for record in records]
            elif a:
                domain &= Domain('department_id', '=', a)
                records = self.search(domain)
                return [(record.id, record.display_name) for record in records]
            elif h:
                domain &= Domain('hospital_ids.id', '=', h)
                print(domain)
                records = self.search(domain)
                return [(record.id, record.display_name) for record in records]
            return super().name_search(name, domain, operator, limit)
        return super().name_search(name, domain, operator, limit)
