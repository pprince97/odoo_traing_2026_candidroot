from odoo import models, fields

class Student(models.Model):
    _name = 'school.student'
    _inherit=['mail.thread','mail.activity.mixin']
    _description = 'Student'

    name = fields.Char(string='Name',required=True,tracking=True)
    roll_number = fields.Integer(string='Roll Number',tracking=True)
    percentage= fields.Float(string='Percentage',help="Percentage of student")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')],string='Gender',default='male')
    is_active = fields.Boolean(string='Is active student?',default=True)
    dob= fields.Date(string='Date of Birth',copy=False)
    admission = fields.Datetime(string='Admission Datetime')
    remarks = fields.Text(string='Remarks',readonly=True)
    id_proof = fields.Binary(string='Id Proof',attachment=True)
    file_name= fields.Char(string='File Name')
    photo = fields.Image(string='Photo')
    file_name_i= fields.Char(string='File Name1')
    active = fields.Boolean(default=True)
    htm= fields.Html(string='Html code')

    class_id=fields.Many2one('school.class',string='Class',ondelete='cascade')
    # subject_ids=fields.Many2many('school.subject','subject_student_rel','student_id','subject_id',string='Subjects')
    teacher_ids=fields.Many2many('school.teacher','teacher_student_rel','student_id','teacher_id',string='Teachers')

    school_id=fields.Many2one('obj.school',string='School',ondelete='restrict')