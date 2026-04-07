from odoo import fields, models, api

class PosOrder(models.Model):
    _inherit = 'pos.order'

    table_duration = fields.Char(string="Table Duration")
    amount = fields.Float(related="")
    date_table = fields.Datetime(string="Date Table" , compute="_compute_date_table")
    # amount_total = fields.Monetary(related="amount_total")

    # async addProductToOrder(product)

    @api.depends("amount_total")
    def _compute_date_table(self):
        for record in self:
            if not record.amount_total:
                print("record.amount_total ---------->  ",record.amount_total)
                return
            else:
                print("record.date_order  ---------->  ", record.date_order)
                record.date_table = record.date_order
                print("record.date_table ---------->  ", record.date_table)
    #
    # @api.model
    # def _order_fields(self, ui_order):
    #     res = super()._order_fields(ui_order)
    #     res['table_duration'] = ui_order.get('table_duration', "")
    #     return res
