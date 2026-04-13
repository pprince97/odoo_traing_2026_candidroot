from odoo import api, fields, models


class GuestDetailsLine(models.Model):
    _name = 'guest.details'
    _inherit = ['pos.load.mixin']
    _description = 'Guest Details'

    age = fields.Integer(string="Age")
    country_id = fields.Many2one('res.country', string="Nationality")
    gender = fields.Selection([('male','Male'),('female','Female')],string="Gender",default='male')
    order_id = fields.Many2one(comodel_name='pos.order', string='Order')

    @api.model
    def _load_pos_data_fields(self, config):
        return ['age', 'country_id', 'gender', 'order_id']