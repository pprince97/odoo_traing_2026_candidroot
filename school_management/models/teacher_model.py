from odoo import models,fields,api

class Teacher(models.Model):
    _name = 'school.teacher'
    _description = 'Teacher'

    name=fields.Char()
    employee_code=fields.Char()
    exp_years=fields.Integer()
    salary=fields.Integer()
    qualification=fields.Selection([('graduate','Graduate'),('post_graduate','Post Graduate'),
                                    ('phd','PHD')])
    is_permanent=fields.Boolean()
    joining_date=fields.Date()
    last_login=fields.Datetime()
    certificate=fields.Binary()
    image=fields.Image()
    student_ids=fields.Many2many('school.student','student_teacher_rel','teacher_id','student_id',string='Students')
    subject_id=fields.Many2one('school.subject',string='Subject',ondelete='cascade')
    school_id = fields.Many2one('school.school',string='School',ondelete='cascade')
