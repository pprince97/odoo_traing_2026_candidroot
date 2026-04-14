from odoo import api, fields, models

class Profile(models.Model):
    _name = 'user.profile'
    _description = 'User Profile'
    _rec_name = 'name'

    name = fields.Char(string='Name')
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    address = fields.Char(string='Address')

    country_id = fields.Many2one('res.country', string='Country')
    state_id = fields.Many2one('res.country.state', string='State' , domain="[('country_id', '=', country_id)]")
    city_id = fields.Many2one('res.city', string='City' , domain="[('state_id', '=', state_id)]")

    @api.onchange('state_id')
    def _onchange_state(self):
        self.city_id = []

    @api.onchange('country_id')
    def _onchange_country_id(self):
        self.city_id = []
        self.state_id = []
