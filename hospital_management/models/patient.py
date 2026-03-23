from odoo import Command, models, fields, api, _
from odoo.fields import Domain

from odoo.exceptions import ValidationError


class Patient(models.Model):
    _name = 'hospital.patient'
    _inherits = {'res.partner': 'partner_id'}
    _description = 'Patient'

    name = fields.Char(related='partner_id.name', string='Name', readonly=False, inherited=True)
    is_active = fields.Boolean(string='Is Active ?', default=True)
    age = fields.Integer(string='Age')
    dob = fields.Date(string='Date of Birth')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender')
    address = fields.Char(string='Address', readonly=True)
    symptoms = fields.Char(string='Symptoms')
    priority = fields.Selection([('low', 'Low'), ('normal', 'Normal'), ('high', 'High')], string='Priority',
                                default='low')
    report_file = fields.Binary('Report File')
    report_name = fields.Char('Report Name')
    reference_field = fields.Selection([('partner', 'Partner'), ('employee', 'Employee')], string='Reference Field',
                                       default='partner')
    partner_id = fields.Many2one('res.partner', ondelete='restrict', string='Partner', required=True)
    doctor_emp_id = fields.Many2many('hr.employee', 'patient_doctor_emp_rel', 'doctor_emp_id', 'patient_id',
                                     string='Doctor Employee ID')
    admission_id = fields.One2many('hospital.admission', 'patient_id', string='Admission')
    appointment_id = fields.Many2one('hospital.appointment', string='Appointments')
    patient_count = fields.Integer()

    # @api.model_create_multi
    # def create(self, vals):
    #     for rec in vals:
    #         print("---------------rec----------------", rec)
    #         print("---------------------------------", rec['symptoms'])
    #         if not rec['symptoms']:
    #             raise ValidationError(self.env._("Symptoms error !!!!!!!!!!!!!"))
    #     return super(Patient, self).create(vals)

    @api.onchange('dob')
    def onchange_dob(self):
        for rec in self:
            print("---------------rec----------------", rec)
            print("---------------------------------", rec.dob)
            if rec.dob and rec.dob > fields.Date.today():
                raise ValidationError(_("Dob error !!!!!!!!!!!!!"))

    # @api.onchange('symptoms')
    # def onchange_symptoms(self):
    #     for rec in self:
    #         print("---------------rec----------------", rec)
    #         print("---------------------------------", rec.symptoms)
    #         if not rec.symptoms:
    #             raise ValidationError(_("Symptoms error !!!!!!!!!!!!!"))

    @api.model
    @api.readonly
    def name_search(self, name='', domain=None, operator='ilike', limit=100):
        print("nameeeeeeeeeeeeeeeeesearchhhhhhhhhhhhhhhhhhhh")
        if name:
            domain = Domain.OR([Domain('symptoms', 'ilike', name),
                                Domain('name', 'ilike', name)])
            print("domain----------------------------", domain)
            records = self.search(domain)
            return [(rec.id, rec.display_name) for rec in records]
        return super().name_search(name, domain, operator, limit)

    @api.onchange('partner_id')
    def onchange_address(self):
        print('onnnnnnnnnnnnnnnnnnnnnnnnnnnnchangeeeeeeeeeeeeeeeeeeeeee')
        for rec in self:
            print('---------------------------------------')
            rec.address = rec.partner_id.street

    def write(self, vals):
        res = super(Patient, self).write(vals)
        if vals.get('name'):
            print("vals-----------------------------", vals)
            print("self_id-----------------------------", self.id)
            if not self.is_active:
                self.write({
                    'doctor_emp_id': [Command.clear()]
                })
        return res

    def admit_patient(self):
        self.is_active = True
        print(f'/odoo/action-208/{self.appointment_id.id}')

    def create_appointment(self):
        self.env['hospital.appointment'].create(
            {'name': self.name, 'app_date': fields.Date.today(), 'status': 'confirm'})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'hospital.appointment',
            'view_mode': 'list,form',
            'domain': [('name', '=', self.name)]
        }

    def discharge(self):
        self.is_active = False

    def patient_address_server_action(self):
        print("-----------------server action-------------------", self)
        self.address = "Address from server action"

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            if val.get('name'):
                self.env['res.partner'].with_context(teacher=True).create({'name': val.get('name')})
        res = super().create(vals_list)
        return res

    def patient_list(self):
        print("Patient list")
        self.patient_count = self.env['hospital.patient'].search_count([])
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'hospital.patient',
            'view_mode': 'list,form',
        }



class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model_create_multi
    def create(self, vals_list):
        print('dddddddddddddddddddddddd', self.env.context)
        res = super().create(vals_list)
        if self.env.context.get('teacher'):
            for rec in res:
                rec.write({
                    'category_id':[
                        Command.link(1)
                    ],
                })
        return res
