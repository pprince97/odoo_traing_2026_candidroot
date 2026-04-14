from odoo import fields, models, api

class GuestDetails(models.Model):
    _name = 'guest.details'
    _inherit = ['pos.load.mixin']
    _description = 'Guest Details'

    age = fields.Integer('Age')
    nationality = fields.Many2one('res.country', string='Nationality')
    gender = fields.Selection([('male','Male'),('female','Female')], 'Gender')
    order_id = fields.Many2one('pos.order', string='Order')

    # @api.model
    # def _load_pos_data_fields(self, config_id):
    #     return ['age', 'nationality', 'gender','order_id','write_date']

class PosSession(models.Model):
    _inherit = "pos.session"

    def _load_pos_data_models(self, config_id):
        result = super()._load_pos_data_models(config_id)
        result.append('guest.details')
        return result