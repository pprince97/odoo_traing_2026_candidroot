from odoo import models,fields,api

class Subject(models.Model):
    _name = 'school.subject'
    _description = 'Subject'

    name=fields.Char()
    subject_code=fields.Integer()
    max_marks=fields.Integer()
    passing_marks=fields.Integer()
    subject_type=fields.Selection([('theory','Theory'),('practical','Practical')])
    is_optional=fields.Boolean()
    syllabus=fields.Binary()
    reference_material=fields.Binary()
    icon=fields.Image()
    student_ids = fields.Many2many('school.student', 'student_subject_rel',
                                   'subject_id', 'student_id',string='Students')
    teacher_ids = fields.One2many('school.teacher', 'subject_id', string='Teachers')
    school_ids=fields.Many2many('school.school','school_subject_rel','subject_id','school_id',string='Schools')

