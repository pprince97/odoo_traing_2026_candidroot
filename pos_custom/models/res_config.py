from odoo import api, fields, models

class ResConfig(models.TransientModel):
    _inherit = 'res.config.settings'

    guest_details = fields.Boolean('Guest Details',config_parameter='pos_custom.guest_details',
                                   related='pos_config_id.guest_details',readonly=False)
    guest_details_timing = fields.Selection([('order_before','Order Before'),('order_after','Order After')],'Guest Details Timing',
                                            default='order_before',config_parameter='pos_custom.guest_details_timing',
                                            related='pos_config_id.guest_details_timing',readonly=False)
    guest_details_required = fields.Boolean('Guest Details Required',config_parameter='pos_custom.guest_details_required',
                                            related='pos_config_id.guest_details_required',readonly=False)