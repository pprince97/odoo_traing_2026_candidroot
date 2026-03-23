from odoo import models,fields,api
from odoo.exceptions import ValidationError

class BorrowStatusCanceledWizard(models.TransientModel):
    _name = 'wizard.borrow.status.canceled'
    _description = 'Borrow Status Canceled'

    canceled_reason = fields.Char(string='Canceled Reason',required=True)

    def write_cancellation_reason(self):
        if self.canceled_reason:
            borrow = self.env['library.borrow.requests'].search([('serial_number','=',self.env.context.get('serial_number'))],limit=1)
            borrow.write({'cancellation_reason':self.canceled_reason,
                          'state' : 'canceled',
                        'canceled_date' : fields.Datetime.now(),
            })