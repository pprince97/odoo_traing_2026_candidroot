from odoo import fields, models

class TaskModel(models.Model):
    _name = 'custom.task'
    _description = 'custom task'

    name=fields.Char(string='Name')
    description=fields.Text(string='Description')
    task_id=fields.Many2one(comodel_name='custom.task')
    gender=fields.Selection([
        ('male','Male'),
        ('female','Female'),
    ])
    age=fields.Integer()
    height=fields.Float()
    birth_date=fields.Date()
    current_Date=fields.Datetime()
    docs=fields.Binary()
    photo=fields.Image()
    task_status=fields.Boolean()
