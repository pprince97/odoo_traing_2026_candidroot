from odoo import fields, models,api
from datetime import date
from odoo.exceptions import ValidationError

class ReportWizard(models.TransientModel):
    _name = 'report.wizard'
    _description = 'Report Wizard'

    start_date = fields.Date(string='Start Date',required=True)
    end_date = fields.Date(string='End Date',required=True)
    is_returned = fields.Boolean(string='Is Returned')
    student_ids = fields.Many2many('res.partner', string='Students')
    book_ids = fields.Many2many('library.books', string='Books')

    @api.onchange('start_date','end_date')
    def _onchange_date(self):
        if (self.start_date and self.end_date):
            if self.start_date > self.end_date:
                raise ValidationError('End Date must be greater than Start Date.')


    # @api.onchange('start_date','end_date')
    # def _onchange_is_return_date(self):
    #     if self.is_returned:
    #         if not ((self.is_returned < self.end_date) and (self.is_returned > self.start_date)):
    #             raise ValidationError('Return Date must be between End Date and Start Date.')

    def print_history(self):
        pass


    def show_history(self):
        self.ensure_one()
        if self.is_returned:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Report ',
                'res_model': 'library.borrow.request',
                'view_mode': 'list,form',
                'target': 'current',
                'domain': [
                    ()
                ],
                'context': {'form_view_ref': 'library_management.book_history_view_form',
                            'list_view_ref': 'library_management.book_history_view_list'}
        }
        else:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Report ',
                'res_model': 'library.borrow.request',
                'view_mode': 'list,form',
                'target': 'current',
                'domain': [
                    ()
                ],
                'context': {'form_view_ref': 'library_management.book_history_view_form',
                            'list_view_ref': 'library_management.book_history_view_list'}
            }
