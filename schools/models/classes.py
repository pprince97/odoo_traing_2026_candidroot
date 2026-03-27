from odoo import models, fields, api

class School(models.Model):
    _name = 'classes.object'
    _description = 'Classes'

    name = fields.Char(string="Class Name")
    class_strength = fields.Integer(string="Class Strength")
    avg_score = fields.Float(string="Average Score")
    section = fields.Selection(
        [('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D')],
        string="Section"
    )

    is_active = fields.Boolean(string="Status")
    start_date = fields.Date(string="Start Date")
    description = fields.Text(string="Description")
    timetable = fields.Integer(string="Time Table")
    class_img = fields.Image(string="Class Image")


    # 2. Student and class
    # student_ids = fields.One2many('student.object','class_id',string="Student ID")