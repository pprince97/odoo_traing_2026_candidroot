from odoo import models,fields,api,Command

class InheritDoctor(models.Model):
    _inherit = 'res.partner'

    doctor_id = fields.Char(string='Doctor ID')
    department_id = fields.Many2one('hospital.department', ondelete='restrict' ,string='Department')
    experience_year = fields.Float(string='Experience years')
    speciality_description = fields.Text(string='Speciality/Description')
    # did = fields.Integer(default=1)
    appointment_ids = fields.One2many('hospital.appointment', 'doctor_id', string='Appointments')
    hospital_ids = fields.Many2many('hospital.hospital', 'hospital_doctor_rel', 'doctor_id', 'hospital_id',string='Hospitals')
    appointment_count = fields.Integer(compute='_compute_appointment_count')


    @api.model_create_multi
    def create(self, vals):
        if self.env.context.get('doctor'):
            vals[0]['doctor_id'] = self.env['ir.sequence'].next_by_code('doctor.seq') or ('New')
        res = super(InheritDoctor, self).create(vals)
        # did_rev=str(self.did)[::-1]
        # while len(did_rev)<4:
        #     did_rev+='0'
        # did_rev='D'+did_rev[::-1]
        # self.pid+=1
        # for rec in res:
        #     rec.write({
        #         'patient_id': did_rev,
        #     })
        for rec in res:
            self.env['res.users'].create({
                'partner_id': rec.id,
                'name': rec.name,
                'email': rec.email,
                'phone': rec.phone,
                'login': rec.name,
                'password': rec.name,
                'group_ids': [Command.set([self.env.ref('hospital_management_tanisha.group_hospital_doctor').id])],
            })
        return res

    def _compute_appointment_count(self):
        self.appointment_count = self.env['hospital.appointment'].search_count([('doctor_id', '=', self.id)])

    def doctor_appointments(self):
        dom = {
            'name': self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'hospital.appointment',
            'view_mode': 'list,form',
            'domain': [('doctor_id', '=', self.id)],
            'context': {'default_doctor_id': self.id},
            'target': 'self'
        }
        if self.appointment_count == 1:
            dom['view_mode'] = 'form'
            dom['res_id'] = self.env['hospital.appointment'].search([('doctor_id', '=', self.id)]).id
        return dom
