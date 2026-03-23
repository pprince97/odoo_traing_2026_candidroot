from odoo import models, fields, api


class Hospital(models.Model):
    _name = 'hospital.hospital'
    _description = 'Hospital Model'
    _rec_name = 'hospital_name'

    hospital_name = fields.Char(string='Hospital Name', required=True)
    address = fields.Char(string='Address')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    registration_number = fields.Char(string='Registration Number')
    description = fields.Text(string='Description')
    department_ids = fields.Many2many('hospital.department', 'hospital_department_rel', 'hospital_id', 'department_id',
                                      string='Departments')
    doctor_ids = fields.Many2many('res.partner', 'hospital_doctor_rel', 'hospital_id', 'doctor_id', string='Doctors',domain="[('department_id','in',department_ids),('doctor_id','like','D%')]")
    patient_ids = fields.Many2many('res.partner', 'hospital_patient_rel', 'hospital_id', 'patient_id',
                                   string='Patients',domain=[('patient_id','like','P%')])
    appointment_ids = fields.One2many('hospital.appointment', 'hospital_id', string='Appointments')
    p_counts = fields.Integer(string='Number of Patients',compute='_compute_p_count')
    d_counts = fields.Integer(string='Number of Doctor',compute='_compute_d_count')
    a_counts = fields.Integer(string='Number of Appointments',compute='_compute_a_count')

    def _compute_p_count(self):
        print('compute>>>>>>>>>>>>>>>>p')
        self.p_counts = self.env['res.partner'].search_count( [('patient_id', 'like', 'P%'),
             ('hospital_ids_.id', '=', self.id)])

    def _compute_d_count(self):
        print('compute>>>>>>>>>>>>>>>>d')
        self.d_counts = self.env['res.partner'].search_count(
            [('doctor_id', 'like', 'D%'), ('department_id', 'in', self.department_ids.ids),
             ('hospital_ids', 'in', self.ids)])

    def _compute_a_count(self):
        self.a_counts = self.env['hospital.appointment'].search_count(
            [('department_id', 'in', self.department_ids.ids),
             ('hospital_id', '=', self.id)])

    def view_doctor(self):
        # print(self.d_count, '>>>>>>>>>>>>>>>>>>>>')
        dd = {
            'name': self.hospital_name,
            'type': 'ir.actions.act_window',
            'res_model': 'res.partner',
            'view_mode': 'list,form',
            'domain': [('doctor_id', 'like', 'D%'), ('department_id', 'in', self.department_ids.ids),
                       ('hospital_ids', 'in', self.ids)],
            'context': {'list_view_ref': 'hospital_management_urvi.doctor_list_view',
                        'form_view_ref': 'hospital_management_urvi.doctor_form_view'},
            'target': self
        }
        if self.d_counts == 1:
            dd['view_mode'] = 'form'
            dd['res_id'] = self.env['res.partner'].search(
                [('doctor_id', 'like', 'D%'), ('department_id', 'in', self.department_ids.ids),
                 ('hospital_ids', '=', self.id)]).id
        return dd

    def view_appointment(self):
        ad = {
            'name': self.hospital_name,
            'type': 'ir.actions.act_window',
            'res_model': 'hospital.appointment',
            'view_mode': 'list,form',
            'domain': [('department_id', 'in', self.department_ids.ids),
             ('hospital_id', '=', self.id)],
            'target': self
        }
        if self.a_counts == 1:
            ad['view_mode'] = 'form'
            ad['res_id'] = self.env['hospital.appointment'].search(
                [('department_id', 'in', self.department_ids.ids),
                 ('hospital_id', '=', self.id)]).id
        return ad

    def view_patient(self):
        # print(self.p_count, '>>>>>>>>>>>>>>>>>>>>>>>>>')
        pd = {
            'name': self.hospital_name,
            'type': 'ir.actions.act_window',
            'res_model': 'res.partner',
            'view_mode': 'list,form',
            'domain': [('patient_id', 'like', 'P%'),
                       ('hospital_ids_.id', '=', self.id)],
            'context': {'list_view_ref': 'hospital_management_urvi.patient_list_view',
                        'form_view_ref': 'hospital_management_urvi.patient_form_view'},
            'target': self
        }
        if self.p_counts == 1:
            pd['view_mode'] = 'form'
            pd['res_id'] = self.env['res.partner'].search(
                [('patient_id', 'like', 'P%'),
                 ('hospital_ids_.id', '=', self.id)]).id
        return pd

    def write(self, vals):
        print(self.patient_ids,'>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        print(self.doctor_ids,'>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        res = super(Hospital,self).write(vals)
        return res

    def create_appointment(self):
        return{
            'type': 'ir.actions.act_window',
            'res_model': 'department.wizard',
            'view_mode': 'form',
            'target': 'new'
        }

