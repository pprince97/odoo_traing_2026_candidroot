from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    pos_config_id = fields.Many2one('pos.config')

    guest_details = fields.Boolean(related="pos_config_id.guest_details", readonly=False)
    guest_details_timing = fields.Selection(
        related="pos_config_id.guest_details_timing",
        readonly=False,
    )
    guest_details_required = fields.Boolean(
        related="pos_config_id.guest_details_required",
        readonly=False,
    )