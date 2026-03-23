from odoo import fields,models,api

class CancelWizard(models.TransientModel):
    _name = 'cancel.wizard'
    _description = 'Cancel Wizard'

    reason = fields.Char(string="Reason",required=True)

    def wizard_cancel_create(self):
        b_r = self.env.context.get('borrow_request')
        res= self.env['library.borrow.request'].search([('id','=',b_r)]).write({'cancellation_reason':self.reason,'state':'canceled','canceled_date':fields.Date.today()})
        return res
