from odoo import models, fields, api

class PosOrder(models.Model):
    _inherit = 'pos.order'

    total_duration = fields.Char(string="Total Duration")

    # @api.model
    # def has_draft_order(self, table_id):
    #     return bool(self.search([('table_id', '=', table_id), ('state', '=', 'draft')], limit=1))