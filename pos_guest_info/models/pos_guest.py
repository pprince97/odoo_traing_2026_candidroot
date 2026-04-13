from odoo import fields, models, api

class PosGuest(models.Model):
    _name = 'pos.guest'
    _inherit = ['pos.load.mixin']

    order_id = fields.Many2one('pos.order')

    age = fields.Integer(string='Age')
    country = fields.Char(string='Country')
    gender = fields.Char(string='Gender')

    @api.model
    def _load_pos_data_fields(self, config_id):
        return ["id", "age", "country", "gender", "write_date"]