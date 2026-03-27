from odoo import models, fields, api

class Teachers(models.Model):
    _name = 'school.teachers'
    _description = 'Teachers'

    name = fields.Char(string='Name')
    employee_code = fields.Char(string='Employee Code')
    experience = fields.Float(string='Experience')
    salary = fields.Float(string='Salary')
    qualification = fields.Selection([('graduate', 'Graduate'),('post_graduate', 'Post Graduate'),('phd','PHD')],string='Qualification')
    is_permanent = fields.Boolean(string='Is Permanent')
    joining_date = fields.Date(string='Joining Date')
    last_login = fields.Datetime(string='Last Login')
    certificate = fields.Binary(string='Certificate')
    image = fields.Image(string='Image')

    student_ids = fields.Many2many('school.students','student_teacher_rel','teacher_id','student_id',string='Students')
    subject_id=fields.Many2one('school.subjects',string='Subjects')
    school_id = fields.Many2one('school.school',string='Schools')