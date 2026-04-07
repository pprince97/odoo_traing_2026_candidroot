from odoo import api, fields, models

class RestaurantTable(models.Model):
    _inherit = 'restaurant.table'

    timer = fields.Datetime()