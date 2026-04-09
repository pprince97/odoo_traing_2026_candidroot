from odoo import api, fields, models

class PosOrder(models.Model):
    _inherit = 'pos.order'

    start_time = fields.Datetime('Start Time')
    end_time = fields.Datetime('End Time')
    dif = fields.Char('Difference (Hours)', compute='_compute_time_diff', store=True)
    male_no = fields.Integer(string='No. of Male')
    female_no = fields.Integer(string='No. of Female')
    guest_no = fields.Integer(string='No. of Female')
    guest_ids = fields.Many2many('pos.guest','pos_order_guest_rel','order_id','guest_id','Guests')

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
        # This tells the backend to pick up 'guest_ids' from the JSON sent by JS
        res = super(PosOrder, self)._order_fields(ui_order)
        res['guest_ids'] = ui_order.get('guest_ids', [])
        return res

    # @api.model
    # def _order_fields(self, ui_order):
    #     res = super()._order_fields(ui_order)
    #     res['start_time'] = ui_order.get('start_time')
    #     res['end_time'] = ui_order.get('end_time')
    #     return res

# class PosSession(models.Model):
#     _inherit = 'pos.session'
#
#     def _load_pos_data_models(self, config_id):
#         data = super()._load_pos_data_models(config_id)
#         data += ['res.country']
#         return data


