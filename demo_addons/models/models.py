from odoo import models,fields,api


class DemoObject(models.Model):
    _name = 'demo.object'
    _description = 'Demo Object'

    name=fields.Text()
    age=fields.Integer()
    phone=fields.Char()
    email=fields.Char()
