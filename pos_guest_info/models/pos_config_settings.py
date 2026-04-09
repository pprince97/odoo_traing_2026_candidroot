from odoo import models, fields

class PosConfig(models.Model):
    _inherit = "pos.config"

    guest_details = fields.Boolean("Guest Details")
    guest_details_timing = fields.Selection(
        [("order_before", "Order Before"), ("order_after", "Order After")],
        default="order_before",
    )
    guest_details_required = fields.Boolean("Guest Details Required")