from odoo import fields, models, api
from odoo.exceptions import ValidationError


class BookBorrowHistoryWizard(models.TransientModel):
    _name = 'book.borrow.history.wizard'
    _description = 'Book Borrow History Wizard'

    start_date = fields.Date('Start Date', required=True)
    end_date = fields.Date('End Date', required=True)
    is_return_date = fields.Boolean('Is Return Date', required=True)
    library_book_borrow_lines_ids = fields.Many2many(
        'library.book.borrow.lines', 'book_borrow_history_wizard_library_book_borrow_lines_rel', 'book_borrow_request_wizard_id', 'library_book_borrow_line_id',
        string='Book Borrowed History Lines'
    )
    student_ids = fields.Many2many('res.users', 'student_book_borrow_history_rel', 'book_borrow_history_id',
                                   'student_id',
                                   domain="[('is_student', '=', True)]", string='Students')
    book_ids = fields.Many2many('library.book', 'book_book_borrow_history_rel', 'book_borrow_history_id', 'book_id',
                                string='Books')

    @api.onchange('end_date')
    def _onchange_end_date(self):
        for rec in self:
            if rec.end_date and rec.start_date and rec.end_date < rec.start_date:
                raise ValidationError('Invalid End Date!')


    def print_book_borrow_history(self):
        print(self.book_ids.ids)
        self.ensure_one()
        if self.is_return_date:
            lines = self.env['library.book.borrow.lines'].search([
                ('return_date_book', '<=', self.end_date),
                ('return_date_book', '>=', self.start_date),
                ('book_id', 'in', self.book_ids.ids),
                ('borrow_req_id.student_id', 'in', self.student_ids.ids),
            ])

            self.library_book_borrow_lines_ids = [(6, 0, lines.ids)]
        else:
            self.library_book_borrow_lines_ids = self.env['library.book.borrow.lines'].search([
                ('book_id', 'in', self.book_ids.mapped('id')),
                ('borrow_req_id.student_id', 'in', self.student_ids.mapped('id')),
            ]).ids
        return self.env.ref('library_management_smit.action_report_book_history').report_action([])
