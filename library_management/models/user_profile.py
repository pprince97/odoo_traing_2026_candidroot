from odoo import fields, models, api


class ProfileSection(models.Model):
    _name = 'user.profile'
    _description = 'User Profile Section'

    name = fields.Char(string='Name')
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')

    country_id = fields.Many2one("res.country", string='Country')
    state_id = fields.Many2one("res.country.state", string='State', domain="[('country_id','=',country_id)]")
    city_id = fields.Many2one("res.city", string='City', domain="[('state_id','=',state_id)]")

    city_text = fields.Char(string='City (Text)')

    address = fields.Char(string='Address')
    zip_code = fields.Char(string='Zip Code')

    user_image = fields.Binary(string='User Image')

    @api.onchange('country_id')
    def _onchange_country_id(self):
        self.state_id = False
        self.city_id = False
        self.city_text = False

    @api.onchange('state_id')
    def _onchange_state_id(self):
        self.city_id = False
        self.city_text = False
