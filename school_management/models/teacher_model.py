from odoo import models, fields

class Teacher(models.Model):
    _name = 'school.teacher'
    _description = 'Teacher Model'

    name = fields.Char(string='Name')
    employee_code = fields.Char(string='Employee Code')
    experience_years= fields.Integer(string='Experience Years')
    salary = fields.Float(string='Salary')
    qualification = fields.Selection([('graduate','Graduate'),('post_graduate','Post Graduate'),('phd','PHD')],string='Qualification',default='graduate')
    is_permanent = fields.Boolean(string='Is Permanent',default=True)
    joining_date = fields.Datetime(string='Joining Date')
    last_login = fields.Datetime(string='Last Login')
    certificate= fields.Binary(string='Certificate')
    image= fields.Image(string='Image')
    student_ids = fields.Many2many('school.student','student_tech_rel','teacher_id','student_id',string='Students')
    subject_id = fields.Many2one('school.subject',string='Subject',ondelete='cascade')
    school_id = fields.Many2one('school.school',string='School',ondelete='cascade')