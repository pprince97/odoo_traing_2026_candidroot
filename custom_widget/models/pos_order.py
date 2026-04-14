from odoo import fields, models, api
from datetime import datetime
from zoneinfo import ZoneInfo

class PosOrder(models.Model):
    _inherit = 'pos.order'

    table_duration = fields.Char(string="Table Duration")
    amount = fields.Float(related="")
    date_table = fields.Datetime(string="Date Table" )
    # amount_total = fields.Monetary(related="amount_total")

    # async addProductToOrder(product)

    #
    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            time_1 = datetime.now(ZoneInfo('Asia/Kolkata'))
            time_2 = time_1.replace(tzinfo=None)
            val["date_table"] = time_2
        res = super().create(vals_list)
        return res

