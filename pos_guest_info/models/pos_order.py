from odoo import models, fields, api

class PosOrder(models.Model):
    _inherit = "pos.order"

    guest_ids = fields.One2many('pos.guest', 'order_id', string="Guest")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # Look for guest_ids in the values coming from JS
            print(vals)
            if 'guest_ids' in vals:
                print("!!! CREATE CAUGHT GUEST_IDS !!!", vals['guest_ids'])
        return super().create(vals_list)

    def write(self, vals):
        if 'guest_ids' in vals:
            print("!!! WRITE CAUGHT GUEST_IDS !!!", vals['guest_ids'])
        return super().write(vals)