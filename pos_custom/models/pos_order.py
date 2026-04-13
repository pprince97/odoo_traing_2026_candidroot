from odoo import api, fields, models

class PosOrder(models.Model):
    _inherit = 'pos.order'

    table_selected = fields.Datetime('Table Join')
    table_left = fields.Datetime('Table Leave')

    total_no_of_guests = fields.Integer('Total No of Guests', store=True)
    no_of_male = fields.Integer('No of Male', store=True)
    no_of_female = fields.Integer('No of Female', store=True)
    guest_ids = fields.One2many('guest.details','order_id',string='Guest Details')

    # @api.model
    # def _order_fields(self, ui_order):
    #     res = super()._order_fields(ui_order)
    #     if 'guest_ids' in ui_order:
    #         res['guest_ids'] = ui_order['guest_ids']
    #     return res