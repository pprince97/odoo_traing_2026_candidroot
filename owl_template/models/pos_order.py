from odoo import api, fields, models

class PosOrder(models.Model):
    _inherit = 'pos.order'

    start_time = fields.Datetime('Start Time')
    end_time = fields.Datetime('End Time')
    dif = fields.Char('Difference (Hours)', compute='_compute_time_diff', store=True)
    male_no = fields.Integer(string='No. of Male')
    female_no = fields.Integer(string='No. of Female')
    guest_no = fields.Integer(string='No. of Female')
    guest_ids = fields.One2many('pos.guest','order_id', 'Guests')

    @api.depends('end_time')
    def _compute_time_diff(self):
        for order in self:
            if order.start_time and order.end_time:
                diff = order.end_time - order.start_time
                order.dif = str(diff)
            else:
                order.dif = "N/A"


    # def write(self, values):
    #     res = super(PosOrder, self).write(values)
    #     guest_orders = self
    #     print('>>>>>>>>>>>>>>>>>>>>',guest_orders)
    #     for order in guest_orders:
    #         guest_detail_list = []
    #         remaining_male = order.male_no - len(order.guest_ids.filtered(
    #             lambda x: x.gender == 'male')
    #         )
    #         remaining_female = order.female_no - len(order.guest_ids.filtered(
    #             lambda x: x.gender == 'female')
    #         )
    #         print('-------------------------------------',remaining_male)
    #         if order.state in ('paid', 'invoiced'):
    #             for male in range(0, abs(remaining_male)):
    #                 guest_detail_list += [(0, 0, {
    #                     'gender': 'male',
    #                     'age':456,
    #                 })]
    #             # for female in range(0, abs(remaining_female)):
    #             #     guest_detail_list += [(0, 0, {
    #             #         'gender': 'female',
    #             #         'config_id': order.config_id.id if order.config_id else False,
    #             #         'company_id': order.company_id.id if order.company_id else False,
    #             #         'session_id': order.session_id.id if order.session_id else False,
    #             #         'country_id': order.company_id.country_id.id if order.company_id.country_id else False,
    #             #         'user_id': order.user_id.id if order.user_id else False
    #             #     })]
    #         if guest_detail_list:
    #             order.guest_ids = guest_detail_list
    #     return res


    # @api.model
    # def _process_order(self, order, existing_order):
    #     # 1. Let the standard process create the order and get the real ID
    #     pos_order = super()._process_order(order, existing_order)
    #
    #     # 2. Find guests synced with this order's UUID
    #     # Note: You must ensure 'pos.order.guest' records are also synced to the server
    #     order_uuid = order.get('uuid')
    #     guests = self.env['pos.order.guest'].search([('pos_order_uuid', '=', order_uuid)])
    #
    #     if guests:
    #         # 3. Link them to the real backend ID
    #         guests.write({'order_id': pos_order})
    #
    #     return pos_order

    # @api.model
    # def _order_fields(self, ui_order):
    #     # This tells the backend to pick up 'guest_ids' from the JSON sent by JS
    #     res = super(PosOrder, self)._order_fields(ui_order)
    #     res['guest_ids'] = ui_order.get('guest_ids', [])
    #     return res

    # @api.model
    # def _order_fields(self, ui_order):
    #     res = super()._order_fields(ui_order)
    #     res['start_time'] = ui_order.get('start_time')
    #     res['end_time'] = ui_order.get('end_time')
    #     return res

class PosSession(models.Model):
    _inherit = 'pos.session'

    @api.model
    def _load_pos_data_models(self, config_id):
        data_models = super()._load_pos_data_models(config_id)
        data_models.append('pos.guest')
        return data_models

