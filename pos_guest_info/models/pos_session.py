from odoo import models, fields, api

class PosOrder(models.Model):
    _inherit = "pos.session"

    def _load_pos_data_models(self, config_id):
        # print("called!!!!!!!!    pos.session, load module")
        res = super()._load_pos_data_models(config_id)
        print("called bbbbbbbbbbbbbbbbbbbbbbbb!!!!!!!!    ressssssssssssss", res)
        res += ['pos.guest']
        print("called aaaaaaaaaaaaaaaaaaaaaaaa!!!!!!!!    ressssssssssssss", res)
        return res