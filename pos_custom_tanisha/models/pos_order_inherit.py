from odoo import api, fields, models

class PosOrder(models.Model):
    _inherit = 'pos.order'

    start_date_time = fields.Datetime()
    end_date_time = fields.Datetime()

    guest_data = fields.Json(string="Guest Data")

    def _order_fields(self, ui_order):
        res = super()._order_fields(ui_order)
        res['guest_data'] = ui_order.get('guest_data', {})
        return res



class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    guest_details_bool = fields.Boolean("Guest Details")
    guest_details_timing = fields.Selection([('order_before','Order Before'),('order_after','Order After')],string="Guest Details Timing", default='order_before')
    guest_details_req_bool = fields.Boolean("Guest Details Required")


