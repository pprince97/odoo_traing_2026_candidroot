from odoo import fields, models

class GuestDetails(models.Model):
    _name = 'guest.details'
    _description = 'Guest Details'

    age = fields.Integer('Age')
    nationality = fields.Many2one('res.country',string='Nationality')
    gender = fields.Selection([('male','Male'),('female','Female')],'Gender')
    order_id = fields.Many2one('pos.order',string='Order',store=True)
