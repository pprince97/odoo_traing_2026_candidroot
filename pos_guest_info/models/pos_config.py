from odoo import fields, models
class PosConfig(models.Model):
    _inherit = 'pos.config'

    # group_analytic_accounting = fields.Boolean(string='Analytic Accounting', implied_group='analytic.group_analytic_accounting')
    guest_details = fields.Boolean(string='Guest Details')
    guest_details_timing = fields.Selection(
        [("order_before", "Order Before"), ("order_after", "Order After")],
        string="Guest Details Timing",
        default="order_before",
    )
    guest_details_required = fields.Boolean(string='Guest Details Required')

