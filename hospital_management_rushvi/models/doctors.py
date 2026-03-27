from odoo import models,fields,api
# from odoo.fields import Domain

class Doctors(models.Model):
    _inherit = 'res.partner'

    doctor_code = fields.Char(string='Doctor Code',readonly=True)
    department_id = fields.Many2one('hospital.management.departments',string='Department')
    experience = fields.Integer("Experience Years")
    speciality = fields.Text("Speciality")
    hospital_ids = fields.Many2many('hospital.management.hospitals','hospital_doctor_rel','doctor_id','hospital_id',string='Doctors')
    doc_appointment_ids = fields.Many2one('hospital.management.appointments','doctor_id')
    doc_appointment_count = fields.Integer(compute='_compute_doc_appointment_count')

    # @api.model_create_multi
    # def create(self, vals_list):
    #     res = super(Doctors,self).create(vals_list)
    #     docs = self.env['res.partner'].search_count([('category_id','=','Doctor')])
    #     tag_doc = self.env['res.partner.category'].search([('name', '=', 'Doctor')], limit=1)
    #     for rec in res:
    #         rec.doctor_code = f"D{docs+1:05d}"
    #         if not rec.patient_code:
    #             rec.category_id =[(4,tag_doc.id)]
    #     return res

    # @api.model_create_multi
    # def create(self, vals_list):
    #     res = super(Doctors, self).create(vals_list)
    #     if self.env.context.get('doctor'):
    #         for rec in res:
    #             rec.doctor_code = self.env['ir.sequence'].next_by_code('doctor.seq') or 'New'
    #     return res

    @api.model_create_multi
    def create(self, vals_list):
        res = super(Doctors, self).create(vals_list)

        if self.env.context.get('doctor') or self.env.context.get('new_doctor'):
            for rec in res:
                if not rec.doctor_code:
                    rec.doctor_code = self.env['ir.sequence'].next_by_code('doctor.seq') or 'New'
                    group_doctor = self.env.ref('hospital_management_rushvi.group_hospital_doctor')
                    self.env['res.users'].create({
                        'name': rec.name,
                        'email': rec.email,
                        'login': rec.email,
                        'password': rec.email,
                        'group_ids': [(4, group_doctor.id)],
                        'partner_id':rec.id,
                    })

        return res

    @api.depends('doc_appointment_ids')
    def _compute_doc_appointment_count(self):
        for rec in self:
            rec.doc_appointment_count = self.env['hospital.management.appointments'].search_count([('doctor_id', 'in', rec.id)])
            print(">>>>>>>>>>>>>>>>>>>>>>>>", rec.doc_appointment_count)

    def doc_view_appointments(self):
        return {
            'name': 'Appointments',
            'type': 'ir.actions.act_window',
            'res_model': 'hospital.management.appointments',
            'view_mode': 'list,form',
            'domain': [('doctor_id', '=', self.id)],
            'context': {'default_doctor_id': self.id},
            'target': 'current',
        }