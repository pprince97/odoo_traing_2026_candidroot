from odoo import models,fields,api

class Classes(models.Model):
    _name = 'school.classes'
    _description = 'Classes'

    name = fields.Integer(string='Name')
    class_strength = fields.Integer(string='Class Strength')
    average_score = fields.Float(string='Average Score')
    section = fields.Selection([('a','A'),('b','B'),('c','C'),('d','D')],string='Section')
    is_active = fields.Boolean(string='Is Active')
    start_date = fields.Date(string='Start Date')
    description = fields.Text(string='Description')
    timetable = fields.Binary(string='Time Table')
    class_image = fields.Image(string='Class Image')
    stars = fields.Selection([('0', 'Low'),
    ('1', 'Medium'),
    ('2', 'High'),
    ('3', 'Very High'),('4', 'Very High'),('5', 'Very High')])

    student_ids = fields.One2many('school.students','class_id',string='Students')
    school_ids = fields.Many2many('school.school','school_class_rel','class_id','school_id',string='Classes')
