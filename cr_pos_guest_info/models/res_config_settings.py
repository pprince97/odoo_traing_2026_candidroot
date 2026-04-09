from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    guest_details=fields.Boolean(string="Guest Details")
    guest_details_timing=fields.Selection([('before_placing_the_order','Before Placing The Order'),
                                           ('after_placing_the_order','After Placing The Order'),],string="Guest Details Timing")
    guest_details_required=fields.Boolean(string="Guest Details Required")