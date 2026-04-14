from odoo import fields, models, api
from odoo.exceptions import ValidationError


class BookBorrowHistoryWizard(models.TransientModel):
    _name = 'book.borrow.history.wizard'
    _description = 'Book Borrow History Wizard'

    start_date = fields.Date('Start Date', required=True)
    end_date = fields.Date('End Date', required=True)

    @api.onchange('end_date')
    def _onchange_end_date(self):
        for rec in self:
            if rec.end_date and rec.start_date and rec.end_date < rec.start_date:
                raise ValidationError('Invalid End Date!')


    def print_rental_history(self):
        self.ensure_one()
        lines = self.env['rental.object'].search([
            ('return_date', '<=', self.end_date),
            ('return_date', '>=', self.start_date)
        ])
        return self.env.ref('rental_management_system.account_move_report').report_action([])

