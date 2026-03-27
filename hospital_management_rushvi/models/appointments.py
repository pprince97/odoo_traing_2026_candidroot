from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Appointments(models.Model):
    _name = 'hospital.management.appointments'
    _description = 'Appointments'
    _rec_name = 'hospital_id'

    hospital_id = fields.Many2one('hospital.management.hospitals',string='Hospital',store=True)
    patient_id = fields.Many2one('res.partner',string='Patient',domain=[('patient_code','ilike','P%')],store=True)
    department_id = fields.Many2one('hospital.management.departments',string='Department',store=True)
    doctor_id = fields.Many2one('res.partner',string='Doctor',domain="[('doctor_code','ilike','D%')]",store=True)
    appointment_date = fields.Datetime(string="Appointment Date",default=fields.Datetime.now())
    patient_address = fields.Char(string='Patient Address')
    patient_dob = fields.Date(string='Patient DOB')
    patient_age = fields.Integer(string='Patient Age (years)')
    patient_mobile = fields.Char(string='Patient Mobile')
    patient_email = fields.Char(string='Patient Email')
    status = fields.Selection([('new','New'),
                               ('in_progress','In Progress'),
                               ('done','Done'),
                               ('cancelled','Cancelled')],
                              string='Status',default='new')
    appointment_count = fields.Integer(compute='_compute_app_count')

    # allowed_dept_ids = fields.Many2many('hospital.management.departments', compute='_compute_allowed_ids')
    # allowed_doc_ids = fields.Many2many('res.partner', compute='_compute_allowed_ids')

    @api.onchange('appointment_date')
    def _onchange_appointment_date(self):
        if self.appointment_date and self.appointment_date < fields.Datetime.today():
            raise ValidationError("Appointment Date Can't be in the past")

    @api.onchange('patient_id')
    def _onchange_patient_id(self):
        patient = self.env['res.partner'].search([('id','in',self.patient_id)],limit=1)
        if self.patient_id and patient:
            print(patient)
            self.patient_dob = patient.date_of_birth
            self.patient_age = patient.age_years
            self.patient_mobile = patient.phone
            self.patient_email = patient.email
            self.patient_address = patient.street, patient.street2 , patient.city , patient.state_id , patient.zip

    # @api.onchange('department_id')
    # def _onchange_dep_doc(self):
    #     if self.doctor_id:
    #         self.doctor_id = ''

    def in_progress_status(self):
        current_in_progress = self.env['hospital.management.appointments'].search([('status', '=','in_progress')])
        if not current_in_progress:
            self.status = 'in_progress'
        else:
            raise ValidationError("Only 1 appointment at a time in progress")

    def done_status(self):
        self.status = 'done'

    def cancel_status(self):
        self.status = 'cancelled'

    @api.depends('hospital_id','patient_id','doctor_id')
    def _compute_app_count(self):
        apt = self.env['hospital.management.appointments'].search_count([('hospital_id','=',self.hospital_id.id),
                                                                        ('patient_id','=',self.patient_id.id),
                                                                        ('doctor_id','=',self.doctor_id.id)]) - 1
        if apt<=0:
            self.appointment_count = 0
        else:
            self.appointment_count = apt

    def view_appointments(self):
        return {
            'name': 'Appointments',
            'type': 'ir.actions.act_window',
            'res_model': 'hospital.management.appointments',
            'view_mode': 'list,form',
            'domain': [('hospital_id','=',self.hospital_id.id), ('patient_id','=',self.patient_id.id),('doctor_id','=',self.doctor_id.id),('id','!=',self.id)],
            'target': 'current',
        }

    # @api.depends('hospital_id', 'department_id')
    # def _compute_allowed_ids(self):
    #     for rec in self:
    #         dept_domain = []
    #         doc_domain = [('doctor_code', 'ilike', 'D%')]
    #         if rec.hospital_id:
    #             dept_domain = [('id', 'in', rec.hospital_id.department_ids.ids)]
    #             doc_domain.append(('hospital_ids', 'in', rec.hospital_id.id))
    #         if rec.department_id:
    #             doc_domain.append(('department_id', '=', rec.department_id.id))
    #
    #         rec.allowed_dept_ids = self.env['hospital.management.departments'].search(dept_domain)
    #         rec.allowed_doc_ids = self.env['res.partner'].search(doc_domain)
    #
    # @api.onchange('doctor_id')
    # def _onchange_doctor(self):
    #     if self.doctor_id:
    #         self.department_id = self.doctor_id.department_id
            # if self.doctor_id.hospital_ids:
            #     self.hospital_id = self.doctor_id.hospital_ids[0]

    # @api.onchange('department_id','doctor_id','hospital_id')
    # def onchange_doctor_id(self):
    #     doctors = self.env['res.partner']
    #     hospitals = self.env['hospital.management.hospitals']
    #     departments = self.env['hospital.management.departments']
    #     # if self.department_id and self.doctor_id:
    #     #     self.hospital_id = hospitals.search([(self.department_id,'in','department_id'),('id','in',self.doctor_id.ids)],limit=1).hospital_id
    #     #
    #     for rec in self:
    #         if rec.hospital_id and rec.department_id:
    #             rec.doctor_id = doctors.search([('department_id','=',rec.department_id),('hospital_id','=',self.hospital_id)],limit=1).id
    #     #
    #     # if self.hospital_id and self.doctor_id:
    #     #     self.department_id = hospitals.search([('hospital_id','=',self.hospital_id.ids),('doctor_id','=',self.doctor_id.ids)],limit=1).department_id.id
