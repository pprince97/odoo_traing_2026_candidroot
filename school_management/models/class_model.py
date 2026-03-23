from odoo import models,fields,api

class Class(models.Model):
    _name = 'school.class'
    _description = 'Class'

    name=fields.Char()
    class_strength=fields.Integer()
    avg_score=fields.Float()
    section=fields.Selection([('a','a'),('b','b'),('c','c'),('d','d')])
    is_active=fields.Boolean(default=True)
    start_date=fields.Date()
    description=fields.Text()
    timetable=fields.Binary()
    class_image=fields.Image()
    student_ids=fields.One2many('school.student','class_id',string='Students')
    school_ids=fields.Many2many('school.school','school_class_rel','class_id','school_id',string='Schools')