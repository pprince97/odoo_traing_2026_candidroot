from odoo import api, fields, models

class PosOrder(models.Model):
    _inherit = 'pos.order'

    start_time = fields.Datetime('Start Time')
    end_time = fields.Datetime('End Time')
    dif = fields.Char('Difference (Hours)', compute='_compute_time_diff', store=True)

    @api.depends('end_time')
    def _compute_time_diff(self):
        for order in self:
            if order.start_time and order.end_time:
                diff = order.end_time - order.start_time
                order.dif = str(diff)
            else:
                order.dif = "N/A"

    @api.model
    def _order_fields(self, ui_order):
        res = super()._order_fields(ui_order)
        res['start_time'] = ui_order.get('start_time')
        res['end_time'] = ui_order.get('end_time')
        return res

