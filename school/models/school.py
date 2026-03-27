from odoo import models,fields,api

class School(models.Model):
    _name = 'school.school'
    _description = 'School'

    name = fields.Char(string='Name')
    code = fields.Char(string='School Number')
    address = fields.Text(string='Address')

    student_ids = fields.One2many('school.students','school_id',string='Students')
    teacher_ids = fields.One2many('school.teachers','school_id',string='Teachers')
    class_ids = fields.Many2many('school.classes','school_class_rel','school_id','class_id',string='Classes')
    subject_ids = fields.Many2many('school.subjects','school_subject_rel','school_id','subject_id',string='Subjects')
    new_count = fields.Integer(string='New Students')
    progress_count = fields.Integer(string='In progress Students')
    confirm_count = fields.Integer(string='Confirm Students')

    admission_ids = fields.One2many('school.admission','school_id',string='Admissions')

    # def admission_counts(self):
    #     admission = self.env['school.admission']
    #     self.new_count = admission.search_count([
    #         ('school_id', '=', self.id),
    #         ('stage', '=', 'new')
    #     ])
    #     self.progress_count = admission.search_count([
    #         ('school_id', '=', self.id),
    #         ('stage', '=', 'inprogress')
    #     ])
    #     self.confirm_count = admission.search_count([
    #         ('school_id', '=', self.id),
    #         ('stage', '=', 'confirm')
    #     ])

    def new_countt(self):
        admission = self.env['school.admission']
        self.new_count = admission.search_count([
            ('school_id', '=', self.id),
            ('stage', '=', 'new')
        ])
        return {
            'name': 'New Admissions',
            'type': 'ir.actions.act_window',
            'res_model': 'school.admission',
            'view_mode': 'list,form',
            'domain': [('school_id', '=', self.id), ('stage', '=', 'new')],
            'target': 'current',
        }

    def progress_countt(self):
        admission = self.env['school.admission']
        self.progress_count = admission.search_count([
            ('school_id', '=', self.id),
            ('stage', '=', 'inprogress')
        ])
        return {
            'name': 'In Progress Admissions',
            'type': 'ir.actions.act_window',
            'res_model': 'school.admission',
            'view_mode': 'list,form',
            'domain': [('school_id', '=', self.id), ('stage', '=', 'inprogress')],
            'target': 'current',
        }

    def confirm_countt(self):
        admission = self.env['school.admission']
        self.confirm_count = admission.search_count([
            ('school_id', '=', self.id),
            ('stage', '=', 'confirm')
        ])
        return {
            'name': 'Confirmed Admissions',
            'type': 'ir.actions.act_window',
            'res_model': 'school.admission',
            'view_mode': 'list,form',
            'domain': [('school_id', '=', self.id), ('stage', '=', 'confirm')],
            'target': 'current',
        }

    @api.model
    def name_create(self, name):
        record = self.create({'name':name })
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        print(">>>>>>>>>>>>>>>>>>",name)
        print(">>>>>>>>>>>>>>>>>>",record)
        return record.id, record.display_name