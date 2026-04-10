from odoo import fields, models ,api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    # pos_config_id is already defined

    # group_analytic_accounting = fields.Boolean(string='Analytic Accounting', implied_group='analytic.group_analytic_accounting')
    pos_config_id = fields.Many2one('pos.config',string="POS Config")

    guest_details = fields.Boolean(related="pos_config_id.guest_details", string="Guest Details", readonly=False)
    guest_details_timing = fields.Selection(related="pos_config_id.guest_details_timing", string="Guest Details Timing",
                                            readonly=False)
    guest_details_required = fields.Boolean(related="pos_config_id.guest_details_required",
                                            string='Guest Details Required', readonly=False)


