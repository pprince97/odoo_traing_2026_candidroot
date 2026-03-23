from odoo import models,fields,api,Command

class RequestCancelWizard(models.TransientModel):
    _name = 'request.cancel.wizard'
    _description = 'Request Cancel Wizard'

    cancellation_reason = fields.Text(string='Cancellation Reason',required=True)
    canceled_date = fields.Date.today()

    def submit(self):
        if self.env.context.get('cancel_wizard'):
            borrow_request = self.env['library.borrow.request'].search([('id','=',self.env.context.get('cancel_wizard'))])
            borrow_request.write({
                'cancellation_reason': self.cancellation_reason,
                'canceled_date': self.canceled_date,
                'state': 'canceled',
            })
        return {
            'type': 'ir.actions.act_window',
            'target': 'self',
            'res_model': 'library.borrow.request',
            'view_mode': 'list,form',
        }

