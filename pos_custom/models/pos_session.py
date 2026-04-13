from odoo import fields, models

class PosSession(models.Model):
    _inherit = "pos.session"

    def _load_pos_data_models(self, config):
        print(">>>>>>>>><<<<<<<<<<<<<")
        result = super()._load_pos_data_models(config)
        result.append('guest.details')
        return result