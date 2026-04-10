from odoo import models, fields, api

class PosGuestSession(models.Model):
    _inherit = 'pos.session'

    @api.model
    def _load_pos_data_models(self, config):
        data = super()._load_pos_data_models(config)
        data += ['pos.order.guest']
        print("\n\n\n", data)
        return data