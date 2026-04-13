from odoo import models, fields, api

class PosOrder(models.Model):
    _inherit = "pos.order"

    guest_ids = fields.One2many('pos.guest', 'order_id', string="Guest")