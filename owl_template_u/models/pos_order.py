from odoo import models, fields, api

class PosOrder(models.Model):
    _inherit = "pos.order"

    start_time = fields.Datetime(string="Start Time")
    end_time = fields.Datetime(string="End Time")
