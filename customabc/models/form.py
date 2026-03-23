from odoo import models, fields, api

class CustomForm(models.Model):
    _name = 'custom.form'
    _description = 'Custom Form'

    name = fields.Char(string="Name")
    age = fields.Integer(string="Age")
    gender = fields.Selection([("male","Male"),("Female","female")], string="Gender")
    password=fields.Char(string="Password")
    review = fields.Text(string="Review")
