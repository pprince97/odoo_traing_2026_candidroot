from odoo import models,fields,api

class ResConfigGuestDetails(models.TransientModel):
    _inherit = 'res.config.settings'

    guest_details = fields.Boolean(string="Guest Details",config_parameter='library_management.guest_details',
                                   related='pos_config_id.guest_details',readonly=False)
    guest_details_timing = fields.Selection([('order_before','Order Before'),('order_after','Order After')],default='order_before',
                                            string="Guest Details Timing",config_parameter='library_management.guest_details_timing',
                                            related='pos_config_id.guest_details_timing',readonly=False)
    guest_details_required = fields.Boolean(string="Guest Details Required",config_parameter='library_management.guest_details_required',
                                            related='pos_config_id.guest_details_required',readonly=False)
