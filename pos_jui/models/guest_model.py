from odoo import models,fields,api,_

class PosOrderGuest(models.Model):
    _name = "pos.order.guest"
    _description = "Guest Order"
    _inherit = ['pos.load.mixin']

    age = fields.Integer("Age")
    nationality_id = fields.Many2one('res.country',string="Nationality")
    gender = fields.Selection([('male','Male'),('female','Female'),('others','Others')],string="Gender")

class PosSession(models.Model):
    _inherit = 'pos.session'

    def _load_pos_data_models(self, config_id):
        data = super()._load_pos_data_models(config_id)
        data.append('pos.order.guest')
        return data