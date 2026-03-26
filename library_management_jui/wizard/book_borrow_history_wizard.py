from odoo import api, fields, models,_
from odoo.fields import Domain
from odoo.exceptions import ValidationError


class BookBorrowHistory(models.TransientModel):
    _name = 'library.book.borrow.history.wizard'
    _description = 'Book Borrow History'

    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    is_return_date = fields.Boolean(string='Is Return Date')
    student_ids = fields.Many2many('res.partner','book_borrow_student_relation','book_borrow_id','student_id',string='Students')
    book_ids = fields.Many2many('library.books','book_borrow_relation','book_borrow_id','book_id',string='Books')

    borrow_request_lines_id = fields.Many2many('library.borrow.request.lines','borrow_request_history_relation','borrow_history_id','borrow_request_line_id',string='Borrow Request Lines')

    @api.onchange('start_date')
    def _onchange_start_date(self):
        for rec in self:
            if rec.start_date and rec.end_date:
                if rec.start_date > rec.end_date:
                    raise ValidationError(_("start date cannot be greater than end date"))

    @api.onchange('end_date')
    def _onchange_end_date(self):
        self._onchange_start_date()

    def print_history(self):
        request_lines = self.env['library.borrow.request.lines']

        if self.is_return_date:
            domain = Domain('borrow_request_id.return_date','>=',self.start_date)
            domain &= Domain('borrow_request_id.return_date','<=',self.end_date)

            if self.student_ids and self.book_ids:
                domain &= Domain('borrow_request_id.student_id','in',self.student_ids.ids)
                domain &= Domain('book_id', 'in', self.book_ids.ids)

            elif not self.student_ids and self.book_ids:
                domain &= Domain('book_id', 'in', self.book_ids.ids)

            elif not self.book_ids and self.student_ids:
                domain &= Domain('borrow_request_id.student_id','in',self.student_ids.ids)

            self.borrow_request_lines_id = request_lines.search(domain)
            return self.env.ref('library_management_jui.book_borrow_history_action').report_action(self.id)

        else:
            domain = Domain.OR([
                Domain([('borrow_request_id.return_date', '>=', self.start_date),('borrow_request_id.return_date', '<=',self.end_date)]),
                Domain([('borrow_request_id.issue_date', '>=', self.start_date), ('borrow_request_id.issue_date', '<=',self.end_date)]),
                Domain([('borrow_request_id.state', 'in', 'draft')]),
                ])

            if self.student_ids and self.book_ids:
                domain &= Domain('borrow_request_id.student_id','in',self.student_ids.ids)
                domain &= Domain('book_id', 'in', self.book_ids.ids)

            elif not self.student_ids and self.book_ids:
                domain &= Domain('book_id', 'in', self.book_ids.ids)

            elif not self.book_ids and self.student_ids:
                domain &= Domain('borrow_request_id.student_id', 'in', self.student_ids.ids)

            self.borrow_request_lines_id = request_lines.search(domain)
            return self.env.ref('library_management_jui.book_borrow_history_action').report_action(self.id)