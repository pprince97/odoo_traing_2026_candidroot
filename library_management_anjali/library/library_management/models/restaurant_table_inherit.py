from odoo import fields, models

class RestaurantTable(models.Model):
    _inherit = 'restaurant.table'

    start_date = fields.Datetime(string="Start Date")
    end_date = fields.Datetime(string="End Date")

    def _load_pos_data_fields(self, config_id):
        fields = super()._load_pos_data_fields(config_id)
        fields.append('start_date')
        return fields


