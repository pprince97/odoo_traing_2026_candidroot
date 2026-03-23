from odoo import models,fields,api,_
from odoo.exceptions import ValidationError

class BookBorrowHistory(models.TransientModel):
    _name = 'book.borrow.history.wizard'
    _description = 'Book Borrow History'

    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    is_return_date = fields.Boolean(string='Is Return Date')
    student_ids = fields.Many2many('res.partner',string='Student')
    book_ids = fields.Many2many('library.books',string='Book')

    def action_get_report(self):
        if not self.is_return_date:
            domain = [('borrow_request_id.state', '!=', 'cancelled'),
                      '|',('borrow_request_id.issue_date', '>=', self.start_date),('borrow_request_id.issue_date', '=', False),
                      '|',('borrow_request_id.return_date', '<=', self.end_date),('borrow_request_id.return_date', '=', False)]
            if self.student_ids:
                domain.append(('borrow_request_id.student_id', 'in', self.student_ids.ids))
            if self.book_ids:
                domain.append(('book_id', 'in', self.book_ids.ids))
        else:
            domain = [('borrow_request_id.return_date', '>=', self.start_date),('borrow_request_id.return_date', '<=', self.end_date)]
            if self.student_ids:
                domain.append(('borrow_request_id.student_id', 'in', self.student_ids.ids))
            if self.book_ids:
                domain.append(('book_id', 'in', self.book_ids.ids))

        return self.env['library.borrow.request.lines'].search(domain)

    def action_print_report(self):
        # record = self.action_print_report()
        return self.env.ref('library_management.book_borrow_history_report_print').report_action(self)


    @api.onchange('start_date','end_date')
    def _onchange_start_end_date(self):
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError(_('Start Date can not be Greater than End Date'))
