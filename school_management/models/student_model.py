from odoo import models, fields, api

class Student(models.Model):
    _name = 'school.student'
    _description = 'Student Model'

    name = fields.Char(string='Name', help='TEST DEMO Name', index=True, copy=True)
    email = fields.Char(string='Email Address')
    roll_number = fields.Integer(string='Roll Number')
    percentage = fields.Float(string='Percentage', digits=(5, 4))
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender', default='male')
    is_active_student = fields.Boolean(string='Is Active Student', default=True)
    date_of_birth = fields.Date(string='Date of Birth')
    admission_datetime = fields.Datetime(string='Date of Admission')
    remarks = fields.Text(string='Remarks')
    id_proof = fields.Binary(string='ID Proof',attachment=True)
    file_name= fields.Char(string='File Name')
    photo= fields.Image(string='Photo')
    class_id = fields.Many2one('school.class',string='Class',ondelete='cascade')
    subject_ids = fields.Many2many('school.subject','student_sub_rel','student_id','subject_id',string='Subjects')
    teacher_ids = fields.Many2many('school.teacher','student_tech_rel','student_id','teacher_id',string='Teachers')
    school_id = fields.Many2one('school.school',string='School',ondelete='cascade', domain=[('active','=',True)])
    extra_note = fields.Html(string='Extra Note')

    @api.model_create_multi
    def create(self, vals):
        res = super(Student, self).create(vals)
        return res
