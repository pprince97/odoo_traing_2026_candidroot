from odoo import models,fields,api

class Entries(models.Model):
    _name="custom.entry"
    _description="entries of users"

    username=fields.Char()
    userphone=fields.Integer()
    role=fields.Char()
    age=fields.Integer()
    height=fields.Float()
