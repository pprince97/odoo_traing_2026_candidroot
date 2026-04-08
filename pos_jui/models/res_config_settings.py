from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    guest_details =fields.Boolean(config_parameter='pos_jui.guest_details',related='pos_config_id.guest_details', readonly=False)
    guest_details_timing =fields.Selection(config_parameter='pos_jui.guest_details_timing',related='pos_config_id.guest_details_timing', readonly=False)
    guest_details_required =fields.Boolean(config_parameter='pos_jui.guest_details_required',related='pos_config_id.guest_details_required', readonly=False)

class PosConfig(models.Model):
    _inherit = 'pos.config'

    guest_details = fields.Boolean(string="Guest Details")
    guest_details_timing = fields.Selection([('order_before', 'Order Before'), ('order_after', 'Order After')],
                                            string="Guest Details Timing")
    guest_details_required = fields.Boolean(string="Guest Details Required")
