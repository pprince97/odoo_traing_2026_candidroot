from odoo import fields, models, api


class PosOrder(models.Model):
    _inherit = 'pos.order'

    table_number = fields.Integer(related="table_id.table_number")
    no_of_male = fields.Integer(string="No. of Male")
    no_of_female = fields.Integer(string="No. of Female")
    no_of_guest = fields.Integer(string="No. of Guest")

    guest_detail_ids = fields.One2many('guest.detail', 'pos_order_id', string="Guest Details" )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            print(vals.get("no_of_male"),"=-----------------------------------------------------------------")
        leads = super().create(vals_list)
        return leads

    @api.model
    def _order_fields(self, ui_order):
        vals = super()._order_fields(ui_order)
        vals['no_of_male'] = ui_order.get('no_of_male', 0)
        vals['no_of_male'] = ui_order.get('no_of_male', 0)
        vals['no_of_male'] = ui_order.get('no_of_male', 0)
        vals['no_of_male'] = ui_order.get('no_of_male', 0)
        return vals

