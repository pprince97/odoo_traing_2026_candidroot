from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    suitable_for_ids = fields.Many2many(
        'suitable.for',
        string='Suitable For')
    #
    # partner_ids = fields.Many2many(
    #     'res.partner', 'calendar_event_res_partner_rel',
    #     string='Attendees', default=_default_partners)
