from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    guest_details_bool = fields.Boolean(related='pos_config_id.guest_details_bool', readonly=False, config_parameter='pos_custom_tanisha.guest_details_bool')
    guest_details_timing = fields.Selection(related='pos_config_id.guest_details_timing', readonly=False, config_parameter='pos_custom_tanisha.guest_details_timing')
    guest_details_req_bool = fields.Boolean(related='pos_config_id.guest_details_req_bool', readonly=False, config_parameter='pos_custom_tanisha.guest_details_req_bool')

