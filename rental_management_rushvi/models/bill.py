from odoo import models,fields,api

class Customer(models.Model):
    _inherit = "account.move"

    rental_order_id = fields.Many2one('rental.order')
    invoice_amount = fields.Monetary(string="Invoice Amount")