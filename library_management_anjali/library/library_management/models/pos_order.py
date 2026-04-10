from odoo import fields, models, api

class PosOrder(models.Model):
    _inherit = 'pos.order'

    start_date = fields.Datetime(string="Start Date")
    end_date = fields.Datetime(string="End Date")

    guest_male = fields.Integer("Male Guests")
    guest_female = fields.Integer("Female Guests")
    guest_total = fields.Integer("Total Guests")
    guest_detail_ids = fields.One2many('pos.order.guest.details', 'order_id',string="Guest Details List")


    @api.model
    def _order_fields(self, ui_order):
        process_fields = super(PosOrder, self)._order_fields(ui_order)
        process_fields.update({
            'guest_detail_ids': ui_order.get('guest_detail_ids', []),
            'guest_male': ui_order.get('guest_male', 0),
            'guest_female': ui_order.get('guest_female', 0),
            'guest_total': ui_order.get('guest_total', 0),
        })
        return process_fields


    # @api.model
    # def _order_fields(self, ui_order):
    #     res = super()._order_fields(ui_order)
    #     res['start_date'] = ui_order.get('start_date')
    #     res['end_date'] = ui_order.get('end_date')
    #     return res

