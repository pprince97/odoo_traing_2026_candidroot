from odoo import fields, models


class RestaurantTable(models.Model):
    _inherit = 'restaurant.table'

    is_first_time = fields.Boolean(string="First Time")

