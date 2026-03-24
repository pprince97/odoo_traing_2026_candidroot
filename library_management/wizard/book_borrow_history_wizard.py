from odoo import fields, models, api
from odoo.exceptions import ValidationError


class BorrowHistoryWizard(models.TransientModel):
    _name = 'borrow.history'
    _description = 'Book Borrow History Wizard'

    start_date = fields.Date('Start Date', required=True)
    end_date = fields.Date('End Date', required=True)
    is_return_date = fields.Boolean('Is Return Date', required=True)

    library_book_borrow_lines_ids = fields.Many2many(
        'borrow.request.line', 'borrow_history_wizard_request_lines_rel',
        'borrow_history_wizard_id', 'book_borrow_line_id',
        string='Book Borrowed History Lines'
    )

    student_ids = fields.Many2many('res.partner', 'student_book_borrow_history_rel', 'book_borrow_history_id',
                                   'student_id',
                                   domain="[('member', '=', 'student')]", string='Students')

    book_ids = fields.Many2many('library.books', 'book_book_borrow_history_rel', 'book_borrow_history_id', 'book_id',
                                string='Books')

    @api.onchange('end_date')
    def _onchange_end_date(self):
        for rec in self:
            if rec.end_date and rec.start_date and rec.end_date < rec.start_date:
                raise ValidationError('Invalid End Date!')

    def print_book_borrow_history(self):
        print(self.book_ids)
        self.ensure_one()
        if self.is_return_date:
            self.library_book_borrow_lines_ids = self.library_book_borrow_lines_ids.search(
                [('return_date', '<=', self.end_date),
                 ('return_date', '>=', self.start_date),
                 ('book_id', 'in', self.book_ids),
                 ('borrow_request_id.student_id', 'in', self.student_ids)
                 ]
            )
        else:
            self.library_book_borrow_lines_ids = self.library_book_borrow_lines_ids.search([
                ('book_id', 'in', self.book_ids),
                ('borrow_request_id.student_id', 'in', self.student_ids)
            ])
        return self.env.ref('library_management.action_report_book_history').report_action([])
