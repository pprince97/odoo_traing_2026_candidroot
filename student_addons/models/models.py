from odoo import models,fields,api


class StudentObject(models.Model):
    _name='student.object'
    _description='Student Object'

    name=fields.Text()
    roll_no=fields.Integer()
    age=fields.Integer()
    div = fields.Char()
    mentor_name=fields.Text()
