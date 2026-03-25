from odoo import fields, models,api
from datetime import date

class CancelWizard(models.TransientModel):
    _name = 'cancel.wizard'
    _description = 'Cancel Wizard'

    cancellation_reason = fields.Char(string='Cancellation Reason',required=True)
    borrow_request_id = fields.Many2one('library.borrow.request',string='Borrow Request')

    def cancellation_wizard(self):
        for rec in self:
            self.env['library.borrow.request'].cancellation_reason = rec.cancellation_reason