from odoo import models, fields

class Subject(models.Model):
    _name = 'school.subject'
    _description = 'Subject model'

    name = fields.Char(string='Name')
    subject_code = fields.Char(string='Subject Code')
    max_marks = fields.Integer(string='Max Marks')
    passing_marks = fields.Float(string='Passing Marks')
    subject_type = fields.Selection([('theory','Theory'),('practical','Practical')],string='Subject Type',default='theory')
    is_optional = fields.Boolean(string='Is Optional')
    syllabus = fields.Binary(string='Syllabus')
    reference_material = fields.Binary(string='Reference Material')
    icon = fields.Image(string='Icon')
    active = fields.Boolean(string='Active',default=True)
    html = fields.Html(string='HTML')
    student_ids = fields.Many2many('school.student','student_sub_rel','subject_id','student_id',string='Students')
    teacher_ids = fields.One2many('school.teacher','subject_id',string='Teacher')
    school_ids = fields.Many2many('school.school','school_subject_rel','subject_id','school_id',string='School')

