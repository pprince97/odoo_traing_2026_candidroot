from odoo import models, fields, api, _

from odoo.exceptions import ValidationError


class Appointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Appointment'
    _rec_name = 'patient_id'

    hospital_id = fields.Many2one('hospital.hospital', string='Hospital')
    patient_id = fields.Many2one('res.partner', string='Patient', domain="[('patient_id','ilike','P%')]")
    department_id = fields.Many2one('hospital.department', string='Department')
    doctor_id = fields.Many2one('res.partner', string='Doctor', domain="[('doctor_id','ilike','D%')]")
    appointment_date = fields.Date(string='Appointment Date', default=fields.Date.today())
    patient_address = fields.Char(related='patient_id.street', string='Address', store=True)
    patient_dob = fields.Date(related='patient_id.dob', string='Date of Birth', store=True)
    age = fields.Char(related='patient_id.age')
    patient_age = fields.Char(compute='_compute_age_years', store=True, readonly=True)
    patient_mobile = fields.Char(related='patient_id.phone', string='Mobile', store=True)
    patient_email = fields.Char(related='patient_id.email', string='Email', store=True)
    status = fields.Selection(
        [('new', 'New'), ('in_progress', 'In Progress'), ('done', 'Done'), ('cancelled', 'Cancelled')], string='Status',
        default='new')
    appointment_count = fields.Integer(compute='_compute_appointment_count')

    def new_status(self):
        self.status = 'new'

    def in_progress_status(self):
        self.status = 'in_progress'

    def done_status(self):
        self.status = 'done'

    def cancelled_status(self):
        self.status = 'cancelled'

    @api.model_create_multi
    def create(self, vals):
        res = super(Appointment, self).create(vals)
        for rec in res:
            rec.patient_id.patient_appointments()
            rec.doctor_id.patient_appointments()
        return res

    def _compute_appointment_count(self):
        self.appointment_count = self.env['hospital.appointment'].search_count(
            [('hospital_id', '=', self.hospital_id.id), ('patient_id', '=', self.patient_id.id),
             ('doctor_id', '=', self.doctor_id.id)])

    def show_appointments(self):
        dom = {
            'type': 'ir.actions.act_window',
            'res_model': 'hospital.appointment',
            'view_mode': 'list,form',
            'domain': [('hospital_id', '=', self.hospital_id.id), ('patient_id', '=', self.patient_id.id),
                       ('doctor_id', '=', self.doctor_id.id)],
            'target': 'self'
        }
        if self.appointment_count == 1:
            dom['view_mode'] = 'form'
            dom['res_id'] = self.env['hospital.appointment'].search(
                [('hospital_id', '=', self.hospital_id.id), ('patient_id', '=', self.patient_id.id),
                 ('doctor_id', '=', self.doctor_id.id)]).id
        return dom

    @api.onchange('appointment_date')
    def _onchange_appointment_date(self):
        for rec in self:
            if rec.appointment_date and rec.appointment_date < fields.Date.today():
                raise ValidationError(_("Appointment date cannot be in past!!!!!!"))

    @api.depends('age')
    def _compute_age_years(self):
        for rec in self:
            rec.patient_age = str(rec.age).split(' ')[0] + " years"

    # @api.onchange('status')
    # def _onchange_patient_id(self):
    #     patient = self.env['res.partner'].search([('patient_id', 'ilike', 'P%')])
    #     print("-----------------------", patient)
    #     for rec in patient:
    #         print(rec.patient_id)

