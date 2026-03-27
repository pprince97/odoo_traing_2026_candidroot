from odoo import models, fields, api

class BorrowCancelWizard(models.TransientModel):
    _name = 'borrow.cancel.wizard'
    _description = 'Borrow Cancel Wizard'

    borrow_id = fields.Many2one('borrow_request.borrow_request', string="Borrow Request")
    cancellation_reason = fields.Text(string="Cancellation Reason", required=True)

    def action_submit(self):
        self.borrow_id.write({
            'state': 'cancel',
            'cancel_date': fields.Date.today(),
            'cancellation_reason': self.cancellation_reason
        })