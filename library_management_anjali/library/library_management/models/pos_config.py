from odoo import models,fields,api

class PosConfig(models.Model):
    _inherit = 'pos.config'

    guest_details = fields.Boolean(string="Guest Details")
    guest_details_timing = fields.Selection([('order_before', 'Order Before'), ('order_after', 'Order After')],
                                            default='order_before',string="Guest Details Timing")
    guest_details_required = fields.Boolean(string="Guest Details Required")
