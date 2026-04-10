
from odoo import fields, models, api

class RestaurantTable(models.Model):
    _inherit = 'restaurant.table'

    is_first_time = fields.Boolean(string="First Time")

    @api.model
    def _load_pos_data_fields(self, config_id):
        """Override to append the new field to the POS loading list."""
        params = super()._load_pos_data_fields(config_id)
        params.append("is_first_time")
        return params