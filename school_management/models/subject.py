from odoo import models, fields

class Subject(models.Model):
    _name = 'school.subject'
    _description = 'Subject'
    _rec_name='name_s'

    name = fields.Char(string='Name')
    name_s = fields.Char(string='Name')
    maths_marks = fields.Integer(string='Maths Marks')
    science_marks= fields.Integer(string='Science Marks')
    passing_marks_maths = fields.Integer(string='Passing Marks for Maths')
    passing_marks_science = fields.Integer(string='Passing Marks for Science')
    chapters_maths = fields.Integer(string='Chapters of maths')
    chapters_science = fields.Integer(string='Chapters of science')

    # student_ids=fields.Many2many('school.student','subject_student_rel','subject_id','student_id',string='Students')
    # teacher_ids=fields.One2many('school.teacher','subject_id',string='Teacher')
    # school_id3=fields.Many2many('obj.school','school_subject_rel','subject_id','school_id',string='Schools')

