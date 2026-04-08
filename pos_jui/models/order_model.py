from odoo import models,fields,api,_

class OrderModel(models.Model):
    _inherit = "pos.order"

    start_date = fields.Datetime("Start Date")
    end_date = fields.Datetime("End Date")
    differ = fields.Char("Difference(date)",compute="_compute_difference")

    def _compute_difference(self):
        for order in self:
            if order.start_date and order.end_date:
                diff = order.end_date - order.start_date
                order.differ = str(diff)
                print(order.differ,'>>>>>>>>>>>>>>>>>>>>>>>>difference')
            else:
                order.differ = "N/A"