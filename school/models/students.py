from odoo import models, fields, api

class Students(models.Model):
    _name = 'school.students'
    _description = 'Students'

    name = fields.Char(string='Name')
    roll_number = fields.Integer(string='Roll Number')
    percentage = fields.Float(string='Percentage')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')])
    is_active = fields.Boolean(string='Is Active')
    date_of_birth = fields.Date(string='Date of Birth')
    admission_datetime = fields.Datetime(string='Admission Date')
    remarks = fields.Text(string='Remarks')
    id_proof = fields.Binary(string='Id Proof')
    photo = fields.Image(string='Photo')
    # htmlfield = fields.Html(string='Html Field')

    teacher_ids = fields.Many2many('school.teachers','student_teacher_rel','student_id','teacher_id',string='Teachers')
    class_id = fields.Many2one('school.classes',string='Class')
    subject_ids = fields.Many2many('school.subjects','student_subject_rel','student_id','subject_id',string='Subjects')

    school_id = fields.Many2one('school.school',string='School')
    res_partner_ids = fields.One2many('res.partner','student_id',string='Res Partners')