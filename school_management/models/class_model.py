from odoo import models, fields

class Class(models.Model):
    _name = 'school.class'
    _description = 'School Class'

    name = fields.Char(string='Name')
    class_length = fields.Integer(string='Class Length')
    average_score = fields.Float(string='Avarage Score')
    section = fields.Selection([('a','A'),('b','B'),('c','C'),('d','D')],string='Section',default='a')
    is_active = fields.Boolean(string='Is Active')
    start_date = fields.Date(string='Start Date')
    description = fields.Text(string='Description')
    timetable = fields.Binary(string='Timetable')
    class_image= fields.Image(string='Class Image')
    student_ids = fields.One2many('school.student','class_id',string='Student IDs')
    school_ids = fields.Many2many('school.school','school_class_rel','class_id','school_id',string='School IDs')

