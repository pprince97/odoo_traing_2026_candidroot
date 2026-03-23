from odoo import models,fields,api

class BorrowCancel(models.TransientModel):
    _name = 'borrow.cancel.wizard'
    _description = 'Borrow Cancel'

    serial_number = fields.Char(string='Serial Number')
    cancellation_reason = fields.Char(string='Cancellation Reason',required=True)


    def cancel_borrow(self):
        borrow = self.env['library.borrow.request'].search([('serial_number','=',self.serial_number)], limit=1)
        borrow.write({
            'cancelled_date': fields.Date.today(),
            'cancellation_reason': self.cancellation_reason,
            'state': 'cancelled',
        })
        return borrow