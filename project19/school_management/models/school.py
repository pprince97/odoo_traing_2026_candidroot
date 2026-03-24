from odoo import fields,models

class School(models.Model):
    _name='obj.school'
    _description='School'

    name=fields.Char(string='Name')
    address=fields.Text(string='Address')
    phone=fields.Integer(string='Phone')
    email=fields.Char(string='Email')

    student_ids=fields.One2many('school.student','school_id',string='Students')
    class_ids=fields.Many2many('school.class','school_class_rel','school_id','class_id',string='Classes')
    teacher_ids=fields.One2many('school.teacher','school_id2',string='Teachers')
    admission_ids=fields.One2many('admission.form','school_id',string='Admissions')
    # subject_ids=fields.Many2many('school.subject','school_subject_rel','school_id','subject_id',string='Subjects')

    new_count = fields.Integer(invisible=True,readonly=True)
    in_progress_count = fields.Integer(invisible=True,readonly=True)
    confirm_count = fields.Integer(invisible=True,readonly=True)

    def new_count_btn(self):
        admission = self.env['admission.form']
        self.new_count = admission.search_count([
            ("state", "=", "new"),
            ("school_id", "=", self.id),
        ])
        return {
            'name': "New Admission",
            'type': 'ir.actions.act_window',
            'view_mode': 'list,form',
            'res_model': 'admission.form',
            'target': 'self',
            'domain': [
                ("state", "=", "new"),
                ("school_id", "=", self.id),
            ],
        }


    def in_progress_count_btn(self):
        admission = self.env['admission.form']
        self.in_progress_count = admission.search_count([
            ("state", "=", "in_progress"),
            ("school_id", "=", self.id),
        ])
        return {
            'name': "Admission in progress",
            'type': 'ir.actions.act_window',
            'view_mode': 'list,form',
            'res_model': 'admission.form',
            'target': 'self',
            'domain': [
                ("state", "=", "in_progress"),
                ("school_id", "=", self.id),
            ],
        }

    def confirm_count_btn(self):
        admission = self.env['admission.form']
        self.confirm_count = admission.search_count([
            ("state", "=", "confirm"),
            ("school_id", "=", self.id),
        ])
        return {
            'name': "Confirmed Admission",
            'type': 'ir.actions.act_window',
            'view_mode': 'list,form',
            'res_model': 'admission.form',
            'target': 'self',
            'domain': [
                ("state", "=", "confirm"),
                ("school_id", "=", self.id),
            ],
        }
