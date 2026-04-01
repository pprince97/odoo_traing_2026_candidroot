from odoo import models, fields, api

class ServiceRequest(models.Model):
    _name = 'service.request'
    _description = 'Service Request'


    companies_id = fields.Many2one('service.company', string='Company')
    product = fields.Many2one('product.template', string='Service')
    customer_id = fields.Many2one('res.partner', string='Customer')
    category_id = fields.Many2one('service.category', string="Service Category")
    date = fields.Date(string="Service date")

    country_id = fields.Many2one("res.country", string='Country')
    state_id = fields.Many2one("res.country.state", string='State', domain="[('country_id','=',country_id)]")
    city_id = fields.Many2one("res.city", string='City', domain="[('state_id','=',state_id)]")

    address = fields.Char(string="Address")




    @api.onchange('country_id')
    def _onchange_country_id(self):
        self.state_id = False
        self.city_id = False

    @api.onchange('state_id')
    def _onchange_state_id(self):
        self.city_id = False
