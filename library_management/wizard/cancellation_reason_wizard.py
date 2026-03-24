from odoo import models, fields, api


class CancellationReasonWizard(models.TransientModel):
    _name = 'cancellation.wizard'
    _description = 'Cancellation Reason'


    reason = fields.Char(string='Cancellation Reason', required=True)
    borrow_id = fields.Many2one('library.borrow.request', string='Borrow Id', ondelete='cascade')

    def cancellation_request_create(self):
        self.borrow_id.write({
            'state': 'cancelled',
            'cancellation_reason': self.reason,
            'cancelled_date': fields.Datetime.now(),
        })

        # self.ensure_one()
        #
        # res = self.env['library.borrow.request'].write({
        #     'cancellation_reason': str(self.reason)
        # })
        #
        # print("RES-------------------------->", res.cancellation_reason)
        # return res
        # print("=====================>", self.reason)
        #
        # res = self.env['library.borrow.request'].write({'cancellation_reason': self.reason})
        # print("=====================>", res)
        # return res
