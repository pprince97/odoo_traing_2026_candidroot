from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, AccessError


class BookBorrowHistoryWizard(models.TransientModel):
    _name = 'book.borrow.history.wizard'
    _description = 'Book Borrow History Wizard'

    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)
    student_ids = fields.Many2many('res.partner', string="Students")
    book_ids = fields.Many2many('book.book', string="Books")
    library_book_borrow_lines_ids = fields.Many2many('borrow_request_line.borrow_request_line', 'borrow_history_rel',
                                                     'wizard_id', 'borrow_line_id', string="Borrow Lines")
    is_return_date = fields.Boolean(string="Is Return Date", default=True)

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for rec in self:
            if rec.end_date < rec.start_date:
                raise ValidationError("End Date cannot be less than Start Date")
            if rec.start_date > rec.end_date:
                raise ValidationError("Start Date cannot be greater than End Date")

    def print_book_borrow_history(self):
        self.ensure_one()

        if self.env.user.has_group('base.group_system'):
            if self.is_return_date:
                self.library_book_borrow_lines_ids = self.env['borrow_request_line.borrow_request_line'].search([
                    ('return_date', '>=', self.start_date),
                    ('return_date', '<=', self.end_date),
                    ('book_id', 'in', self.book_ids.ids),
                    ('borrow_id.student_id', 'in', self.student_ids.ids)
                ])
            else:
                self.library_book_borrow_lines_ids = self.env['borrow_request_line.borrow_request_line'].search([
                    ('book_id', 'in', self.book_ids.ids),
                    ('borrow_id.student_id', 'in', self.student_ids.ids)
                ])
            return self.env.ref('library_management_sunil.action_report_book_history').report_action(self)

