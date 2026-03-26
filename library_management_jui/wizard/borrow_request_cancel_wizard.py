from odoo import api,fields,models,exceptions

class BorrowRequestCancel(models.TransientModel):
    _name = 'library.borrow.request.cancel.wizard'
    _description = 'Borrow Request Cancel'

    cancellation_reason =fields.Char(string='Cancellation Reason',required=True)
    borrow_request_id = fields.Many2one('library.borrow.request')

    def wizard_submit(self):
        res = self.env['library.borrow.request'].search([('id','=',self.borrow_request_id)])
        res.update({'state':'canceled','canceled_date':fields.Date.today(),'cancellation_reason':self.cancellation_reason})