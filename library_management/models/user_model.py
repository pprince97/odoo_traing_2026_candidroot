from odoo import models,fields

class User(models.Model):
    _name = 'library.user'
    _description = 'Library User Model'

    name = fields.Char(string="User's Name")
    email = fields.Char(string="User's Email")
    phone = fields.Char(string="User's Phone Number")
    age = fields.Integer(string="Age")
    gender = fields.Selection([('male','Male'),('female','Female')],string="Gender")
    address = fields.Char(string="Address")
    id_proof = fields.Binary(string="Proof")
    currency_id = fields.Many2one('res.currency', string='Currency')
    salary = fields.Monetary(string="Salary",currency_id='currency_id')
    active_user = fields.Boolean(string="Active User")
    active_employee = fields.Boolean(string="Active Employee")