from odoo import models,fields,api

class Payment(models.Model):
    _inherit = 'account.payment'

    pay_datetime = fields.Datetime('Payment date & time')
    payment_mode = fields.Selection([('cash', 'Cash'),('online', 'Online')],string="Payment mode")
    payment_id = fields.Char("Payment ID")
