from odoo import models, fields, api, _ , Command
from odoo.fields import Domain

from odoo.exceptions import ValidationError


class Patient(models.Model):
    _name = "hospital.patient"
    _inherit = ["mail.thread" , "mail.activity.mixin"]
    _inherits = {'res.partner': 'partner_id'}
    _description = "Patient Model"

    name = fields.Char(related='partner_id.name', inherited=True, readonly=False)
    is_active = fields.Boolean(string="Is Active Patient")
    partner_id = fields.Many2one('res.partner',string='Partner', required=True, ondelete='restrict')
    age = fields.Integer(string="Age",tracking=True)
    dob = fields.Date(string="Date of Birth")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender", default='male')
    address = fields.Text(string="Address",store=True,readonly=True)
    symptoms = fields.Text(string="Symptoms")
    priority = fields.Selection([('low', 'Low'), ('normal', 'Normal'), ('high', 'High')], string="Priority",default='high')
    doctor_employee_id = fields.Many2one('hr.employee', string="Doctor Employee ID")
    report_file = fields.Binary(string="Report File", attachment=True)
    report_name = fields.Char(string="Report Name")
    reference_field = fields.Selection([('partner', 'Partner'), ('employee', 'Employee')], string="Reference Field",default='partner')
    consultation_fee = fields.Float(string="Consultation_fee", related='doctor_employee_id.consultation_fee',store=True)

    @api.onchange('partner_id')
    def _onchange_partner_address(self):
        print('onchange_partner_address>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        for rec in self:
            rec.address = rec.partner_id.street
            print('\n\n HHHHHHHHHHHHHHh', rec.address)

    @api.onchange('symptoms')
    def _onchange_partner_symptoms(self):
        print('onchange_partner_address>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        for rec in self:
            if rec.symptoms and rec.symptoms=="":
                raise ValidationError('No symptoms')


    @api.model_create_multi
    def create(self, vals):
        res = super(Patient, self).create(vals)
        for rec in res:
            if rec.doctor_employee_id:
                rec.doctor_employee_id.patient_list()
            if rec.name:
                self.env['res.partner'].with_context(patientc=True).create({'name': rec.name})
        return res

    def write(self, vals):
        res = super(Patient, self).write(vals)
        for rec in self:
            if rec.doctor_employee_id:
                rec.doctor_employee_id.patient_list()
        return res

    def admit_patient(self):
        self.is_active = True

    def discharge_patient(self):
        self.is_active = False

    @api.model
    def name_create(self, name):
        record = self.create({'name': name,'is_active':True})
        print('created>>>>>>>>>>>>>>>>>>patient:', name)
        return record.id, record.display_name

    @api.model
    @api.readonly
    def name_search(self, name='', domain=None, operator='ilike', limit=100):
        if self.env.context.get('test'):
            domain = Domain.OR([Domain('name', operator, name),
                       Domain('symptoms', operator, name)])
            records = self.search(domain)
            return [(record.id, record.display_name) for record in records]
        return super().name_search(name, domain, operator, limit)


    # @api.model
    # def name_search(self, name='', domain=None, operator='ilike', limit=100):
    #     domain = domain or []
    #     # optimization for a SOL services name_search, to avoid joining on sale_order with too many lines
    #     if domain and ('is_service', '=', True) in domain and operator in ('like', 'ilike') and limit is not None:
    #         sols = self.search_fetch(
    #             domain, ['display_name'], limit=limit, order='order_id.id DESC, sequence, id',
    #         )
    #         return [(sol.id, sol.display_name) for sol in sols]
    #     return super().name_search(name, domain, operator, limit)

    # @api.depends('complete_name', 'email', 'vat', 'state_id', 'country_id', 'commercial_company_name')
    # @api.depends_context(
    #     'test'
    # )
    # def _compute_display_name(self):
    #     # type_description = dict(self._fields['type']._description_selection(self.env))
    #     for patient in self:
    #         if patient.env.context.get("test"):
    #             name = f"{patient.name} - {patient.symptoms}"
    #             patient.display_name = name.strip()

class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model_create_multi
    def create(self, vals_list):
        print('dddddddddddddddddddddddd',vals_list)
        res = super().create(vals_list)
        if self.env.context.get('patientc'):
            for rec in res:
                rec.write({
                    'category_id': [
                        Command.link(3),
                    ]
                })

        print('get', res.category_id)
        print('name', res.category_id.name)
        return res
