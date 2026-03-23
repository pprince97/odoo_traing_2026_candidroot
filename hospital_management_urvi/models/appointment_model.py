from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Appointment(models.Model):
    _name = "hospital.appointment"
    _description = "Appointment Model"
    _rec_name = "patient_id"

    hospital_id = fields.Many2one('hospital.hospital', string='Hospital', ondelete='cascade')
    patient_id = fields.Many2one('res.partner', string='Patient', ondelete='cascade',
                                 domain=[('patient_id', 'like', 'P%')])
    department_id = fields.Many2one('hospital.department', 'Department', ondelete='cascade')
    doctor_id = fields.Many2one('res.partner', 'Doctor', ondelete='cascade', domain=[('doctor_id', 'like', 'D%')])
    appointment_date_ = fields.Date(string="Appointment Date", default=fields.Date.today())  # cannnot be in the past
    # patient_address = fields.
    patient_dob = fields.Date(related='patient_id.date_of_birth')
    age_ = fields.Char(related='patient_id.age_', string="Age")
    patient_age = fields.Char(compute='_compute_age_years', store=True)
    patient_mobile = fields.Char(related='patient_id.phone')
    patient_email = fields.Char(related='patient_id.email')
    status = fields.Selection(
        [('new', 'New'), ('in_progress', 'In Progress'), ('done', 'Done'), ('cancelled', 'Cancelled')],
        string="Appointment Status", default='new')
    _p_count = fields.Integer(string="In Progress Appointment")
    _date = fields.Date(string='Today', default=fields.Date.today())
    _a_count_ = fields.Integer(string="Appointment count", compute="_compute_a_count")
    allowed_hospitals = fields.Many2many('hospital.hospital')
    user = fields.Many2one(related="patient_id.user_id")


    @api.model_create_multi
    def create(self,vals):
        res = super().create(vals)
        for rec in res:
            rec.current_user = rec.env.user
        return res

    def _compute_a_count(self):
        self._a_count_ = self.env['hospital.appointment'].search_count(
            [('patient_id', '=', self.patient_id.id),
             ('doctor_id', '=', self.doctor_id.id),
             ('id', '!=', self.id),
             ('hospital_id', '=', self.hospital_id.id)])

    def new_status(self):
        self.update({'status': 'new'})

    def in_progress_status(self):
        self._p_count = self.env['hospital.appointment'].search_count(
            [('patient_id', '=', self.patient_id.id), ('status', '=', 'in_progress')])
        if self._p_count == 0:
            self.update({'status': 'in_progress'})
        else:
            raise ValidationError("One Appointment Status is already In Progress")

    def done_status(self):
        self.update({'status': 'done'})

    def cancel_status(self):
        self.update({'status': 'cancelled'})

    @api.onchange('appointment_date_')
    def _onchange_appointment_date(self):
        if self.appointment_date_ and self.appointment_date_ < fields.Date.today():
            self.appointment_date_ = fields.Date.today()
            print(self.appointment_date_)
            raise ValidationError("Appointment Date is Invalid")

    def view_appointments(self):
        a = {
            'name': self.patient_id.name,
            'type': 'ir.actions.act_window',
            'res_model': 'hospital.appointment',
            'view_mode': 'list,form',
            'domain': [('patient_id', '=', self.patient_id.id),
                       ('doctor_id', '=', self.doctor_id.id),
                       ('id', '!=', self.id),
                       ('hospital_id', '=', self.hospital_id.id)],
            'target': 'new'
        }
        if self._a_count_ == 1:
            a['view_mode'] = 'form'
            a['res_id'] = (self.env['hospital.appointment'].search(
                [('patient_id', '=', self.patient_id.id),
                 ('doctor_id', '=', self.doctor_id.id),
                 ('id', '!=', self.id),
                 ('hospital_id', '=', self.hospital_id.id)])).id
        return a

    @api.onchange('doctor_id')
    def _onchange_doctor_id(self):
        if self.doctor_id:
            self.department_id = self.env['res.partner'].search(
                [('id', '=', self.doctor_id.id)]).department_id.id
        else:
            self.department_id = False

    @api.onchange('department_id')
    def _onchange_department_id(self):
        print('onchangeeee', self.allowed_hospitals)
        if self.department_id and self.doctor_id:
            self.allowed_hospitals = self.env['hospital.hospital'].search(
                [('department_ids', 'in', self.department_id.id), ('doctor_ids', 'in', self.doctor_id.id)])
        elif self.department_id:
            self.allowed_hospitals = self.env['hospital.hospital'].search(
                [('department_ids', 'in', self.department_id.id)])
        elif self.hospital_id:
            self.allowed_hospitals = self.env['hospital.hospital'].search([('doctor_ids', 'in', self.doctor_id.id)])
        else:
            self.allowed_hospitals = self.env['hospital.hospital'].search([])
        print('onchangeeee', self.allowed_hospitals)

    @api.depends('age_')
    def _compute_age_years(self):
        for rec in self:
            if rec.age_:
                print(rec.age_)
                rec.patient_age = rec.age_.split()[0] + ' years'
                print(rec.patient_age)
