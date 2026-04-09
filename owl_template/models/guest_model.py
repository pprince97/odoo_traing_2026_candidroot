from odoo import models, fields, api

class Guest(models.Model):
    _name = 'pos.guest'
    _description = 'Guest'

    age = fields.Integer('Age')
    gender = fields.Selection([('male','male'),('female','female')],'Gender')
    country_id = fields.Many2one('res.country','Country')