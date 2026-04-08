from odoo import fields, models, api
from datetime import datetime
from zoneinfo import ZoneInfo


class PosOrder(models.Model):
    _inherit = 'pos.order'

    table_duration = fields.Char(string="Table Duration")
    # amount = fields.Float(related="")
    date_table = fields.Datetime(string="Date Table")
    start_date = fields.Datetime(string="start Date")
    end_date = fields.Datetime(string="End Date")

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            # time_1 = datetime.now(ZoneInfo('Asia/Kolkata'))
            # print("66666666666", time_1)
            time_11 = datetime.today()
            # print("7777777", time_11)
            # time_2 = time_1.replace(tzinfo=None)
            # print("888888888888888", time_2)
            val["start_date"] = time_11
            val["date_table"] = time_11
            print(val["date_table"], " ------val:date_table")
        res = super().create(vals_list)
        return res

    def write(self, vals):
        if vals.get("state") == 'paid':
            vals["end_date"] = datetime.today()
        return super().write(vals)

