from odoo import models, fields, api

class Student(models.Model):
    _name = 'student.object'
    _description = 'Student'
    _inherit = ['mail.thread','mail.activity.mixin']

    name = fields.Char(string="Student Name", required=True, tracking=1, help="School Student Name")
    email = fields.Char(string="Student Email", tracking=1)

    roll_no = fields.Char(string="Roll No", required=True)

    percentage = fields.Float(string="Percentage")

    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female')],
        string="Gender",
        required=True,
        tracking=1
    )

    is_active = fields.Boolean(string="Status")

    dob = fields.Datetime(string="Date of Birth")

    admission_dt = fields.Date(string="Date of Admission")

    remarks = fields.Text(string="Remarks")
    id_proof = fields.Binary(string="ID Proof")
    photo = fields.Image(string="Photo")

    st_html = fields.Html(string="HTML")

    # 1. Teacher and student
    teacher_id = fields.Many2one("teacher.object", string="Teacher", ondelete='restrict')

    # 2. student and class
    class_id = fields.Many2one("classes.object", string="Class")

    # 3. Student and subject
    subject_ids = fields.Many2many("subject.object",'stud_sub_rel','student_id','subject_id', string="Subjects")


    school_id = fields.Many2one('school.object',string='School')

    @api.model_create_multi
    def create(self, vals):
        print("\n\n vals >>>>>>>>>>>", vals)
        vals['name'] = ''
        res = super(Student, self).create(vals)
        print("\n\n res >>>>>>>>>>", res)
        return res