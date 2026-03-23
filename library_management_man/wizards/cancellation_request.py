import datetime

from odoo import models, fields, api

class CancellationRequest(models.TransientModel):
    _name = 'cancellation.request'
    _description = 'Cancellation Request'

    cancellation_reason = fields.Char(string='Cancellation Reason')
    borrow_request_id = fields.Many2one('library.borrow.request', string='Borrow Request')

    def canceled_process(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window_close'
        }

    def canceled_request(self):
        self.borrow_request_id.write({
            'state': 'canceled',
            'canceled_date': datetime.date.today(),
            'cancellation_reason' : self.cancellation_reason,
        })