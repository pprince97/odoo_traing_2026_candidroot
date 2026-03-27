from odoo import models, fields, api

class School(models.Model):
    _name = "school.object"
    _description = "School"

    name = fields.Char(string='School Name', required=True)
    code = fields.Char(string='School Code')
    address = fields.Text(string='Address')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    school_category = fields.Selection([
        ('primary', 'Primary School'),
        ('middle', 'Middle School'),
        ('private', 'Secondary School'),
    ],
        string='School Category',
        default='primary',
    )
    school_img = fields.Binary(string='School Image')
    is_active = fields.Boolean(string='Is Active')

    student_ids = fields.One2many('student.object','school_id',string='Students')

    # school and teacher
    teacher_ids = fields.One2many('teacher.object','school_id',string='Teachers')

    # School and subject
    subject_ids = fields.Many2many('subject.object','school_subject_rel','subject_id','school_id',string='Subjects')

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            val['code'] = "123"
        res = super(School, self).create(vals)
        return res

    def write(self, vals):
        print("\n\n vals  write >>>>>>>>>>", vals)
        vals['code'] = "987"
        res = super(School, self).write(vals)
        print("\n\n res  write >>>>>>>>>>", res)
        return res