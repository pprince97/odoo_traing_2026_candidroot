from odoo import models, fields, api

class PosOrderGuest(models.Model):
    _name = 'pos.order.guest'
    _description = 'POS Order Guest Details'

    order_id = fields.Many2one('pos.order', string="Order")
    age = fields.Integer(string="Age")
    nationality = fields.Char(string="Nationality")
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], string="Gender")