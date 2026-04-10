from odoo import api, fields, models


class GuestDetailsLine(models.Model):
    _name = 'guest.details.line'
    _description = 'Guest Details Line'

    age = fields.Integer(string="Age")
    country_id = fields.Many2one('res.country', string="Nationality")
    gender = fields.Selection([('male','Male'),('female','Female')],string="Gender",default='male')
    pos_order_id = fields.Many2one(comodel_name='pos.order', string='Order')