from odoo import models, fields

class PosOrder(models.Model):
    _inherit = "pos.order"

    start_time = fields.Datetime(string="Start Time")
    end_time = fields.Datetime(string="End Time")

    def write(self, vals):

        if vals.get('state') == "cancel":
            vals['end_time'] = fields.Datetime.now()

        return super().write(vals)