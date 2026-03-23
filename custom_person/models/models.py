from odoo import models, fields, api

class Customperson(models.Model):
    _name="custom.person"
    _description="Custom Person"

    name=fields.Char(string="Name")
    age=fields.Integer(string="Age")
    birthdate=fields.Date(string="Birthdate")
    gender=fields.Selection([('male','Male'),('female','Female')],string="Gender",default='male')
    handicap=fields.Boolean(string="Handicap",default=False)
    percentage=fields.Float(string="Percentage")
    address=fields.Text(string="Address")
    photo=fields.Binary(string="Photo")
    signature=fields.Image(string="Signature")
    current_date=fields.Datetime(string="Current Date")
