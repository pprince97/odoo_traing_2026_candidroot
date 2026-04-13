from odoo import models, fields, api


class PosOrder(models.Model):
    _inherit = "pos.session"

    def _load_pos_data_models(self, config_id):
        # print("called!!!!!!!!    pos.session, load module")
        res = super()._load_pos_data_models(config_id)
        print("called b!!!!    resssss", res)
        res += ['guest.detail']
        print("called aa!!!    resssss", res)
        return res