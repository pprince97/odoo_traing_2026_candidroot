from odoo import models, fields

class ClassModel(models.Model):
    _name = 'school.class'
    _description = 'Class'

    name = fields.Char(string='Name')
    class_str = fields.Integer(string='Class Strength')
    avg_scr= fields.Float(string='Average Score')
    section = fields.Selection([('a','A'),('b','B'),('c','C'),('d','D')],string='Section',default='a')
    is_active = fields.Boolean(string='Is Active?',default=True)
    start_date= fields.Date(string='Start date')
    description = fields.Text(string='Description')
    timetable = fields.Binary(string='Timetable')
    file_name2 = fields.Char(string='File Name4')
    class_image = fields.Image(string='Class Image')
    file_name_i2 = fields.Char(string='File Name5')

    student_ids= fields.One2many('school.student','class_id',string='Student')
    school_ids=fields.Many2many('obj.school','school_class_rel','class_id','school_id',string='School')