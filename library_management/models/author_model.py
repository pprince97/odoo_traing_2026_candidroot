from odoo import models,fields,api

class Author(models.Model):
    _name = 'library.author'
    _description = 'Library Author Model'
    _rec_name = 'author_name'

    author_name = fields.Char(string="Author's Name")
    age = fields.Integer(string="Age")
    mobile = fields.Char(string="Mobile")
    gender = fields.Selection([('male','Male'),('female','Female')],string="Gender")
    is_active = fields.Boolean(string="Is Active")
    description = fields.Text(string="Description")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    photo = fields.Image(string='Photo')
