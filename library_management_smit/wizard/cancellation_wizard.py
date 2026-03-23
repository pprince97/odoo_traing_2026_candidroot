from odoo import fields, models, api


class CancellationWizard(models.TransientModel):
    _name = 'cancellation.wizard'
    _description = 'Cancellation Wizard'

    reason = fields.Char(string="Reason")

    def wizard_cancel_create(self):
        b_r = self.env.context.get('borrow_request')
        res = self.env['library.book.borrow'].search([('id', '=', b_r)]).write({'cancellation_reason': self.reason})
        return res
