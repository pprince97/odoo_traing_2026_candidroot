from odoo import models,fields,api

class Student(models.Model):
    _name = 'school.student'
    _description = 'Student'

    name=fields.Char()
    roll_no=fields.Integer()
    percentage=fields.Float()
    gender=fields.Selection([('male','Male'),('female','Female')])
    is_active_student=fields.Boolean(default=True)
    dob=fields.Date()
    admission_date_time=fields.Datetime()
    remarks=fields.Text()
    id_proof=fields.Binary()
    photo=fields.Image()
    teacher_ids=fields.Many2many('school.teacher','student_teacher_rel','student_id','teacher_id',string='Teachers')
    class_id = fields.Many2one('school.class', string='Class', ondelete='cascade')
    subject_ids=fields.Many2many('school.subject','student_subject_rel',
                                 'student_id','subject_id',string='Subjects')
    school_id = fields.Many2one('school.school',string='School',ondelete='cascade')
    res_ids = fields.One2many('res.partner','student_id',string='Res Partners')

