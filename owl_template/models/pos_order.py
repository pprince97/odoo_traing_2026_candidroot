from odoo import fields, models, api
from datetime import datetime
from zoneinfo import ZoneInfo

class PosOrder(models.Model):
    _inherit = 'pos.order'
 
    table_duration = fields.Char(string="Table Duration")
    amount = fields.Float(related="")
    date_table = fields.Datetime(string="Date Table")

    start_time = fields.Datetime(string="Start Time")
    end_time = fields.Datetime(string="End Time")
 
 
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            time_1 = datetime.now(ZoneInfo('Asia/Kolkata'))
            time_2 = time_1.replace(tzinfo=None)

            vals['start_time'] = fields.Datetime.now()

            vals["date_table"] = time_2
            print("Date Table =======>", vals["date_table"])

        res = super().create(vals_list)
        return res

    def write(self, vals):
        print("\n\n\n===============>", vals)

        if vals.get('state') == 'paid':
            vals['end_time'] = fields.Datetime.now()

        print("\n\n\n==========>", vals.get('state'))

        res = super().write(vals)
        return res
