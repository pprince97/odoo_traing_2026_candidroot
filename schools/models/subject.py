from odoo import models, api, fields

class School(models.Model):
    _name = 'subject.object'
    _description = 'Subject'

    name = fields.Char(string="Subject Name")
    subject_code = fields.Char(string="Subject Code")
    max_marks = fields.Integer(string="Max Marks")
    passing_marks = fields.Integer(string="Passing Marks")
    subject_type = fields.Selection([
        ('theory', 'Theory'),
        ('practical', 'Practical')],
        string="Subject Type"
    )

    is_optional = fields.Boolean(string="Is Optional")
    syllabus = fields.Integer(string="Syllabus")
    reference = fields.Binary(string="Reference")
    icon = fields.Image(string="Icon")


    # 3. Student and subject
    students_ids = fields.Many2many("student.object",'stud_sub_rel','subject_id','student_id', string="Students")

    # 3. Teacher and subject
    teacher_ids = fields.Many2many("teacher.object",'teacher_sub_rel','subject_id','student_id', string="Teacher")

    # school and subject
    school_ids = fields.Many2many('school.object','school_subject_rel','school_id','subject_id', string="School")