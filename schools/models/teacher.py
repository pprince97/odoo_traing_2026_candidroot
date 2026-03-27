from odoo import fields, models, api

class Teacher(models.Model):
    _name = 'teacher.object'
    _description = 'Teacher'
    _inherit = ['mail.thread','mail.activity.mixin']

    name = fields.Char(string="Teacher Name", tracking=True)
    employeeCode = fields.Char(string="Employee Code", tracking=True)
    experience = fields.Char(string="Experience")
    salary = fields.Float(string="Salary")
    qualification = fields.Selection(
        [('graduate', 'Graduate'),
         ('postgraduate', 'Post Graduate'),
         ('phd','PHD')],
        string="Qualification",
        default='graduate',
        tracking=True
    )

    isPermanent = fields.Boolean(string="Status")
    joining_date = fields.Date(string="Joining Date")
    lastLogin = fields.Datetime(string="Last Login Date", tracking=True)
    certificate = fields.Binary(string="Certificate")
    image = fields.Image(string="Image")

    # 7. Student and teacher
    student_ids = fields.One2many("student.object", "teacher_id", string="Students", tracking=True)

    # 10. Teacher and subject
    subject_ids = fields.Many2many("subject.object",'teacher_sub_rel','student_id','subject_id', string="Subject")

    # School and teacher
    school_id = fields.Many2one('school.object',string='School')