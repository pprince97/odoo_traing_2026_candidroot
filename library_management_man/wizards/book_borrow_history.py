from odoo import models, fields, api
from odoo.exceptions import ValidationError


class BookBorrowHistory(models.TransientModel):
    _name = 'book.borrow.history'
    _description = 'Book borrow history'
    _rec_name = 'student_ids'


    start_date = fields.Date(string="Start date", required=True )
    end_date = fields.Date(string="End date", required=True )
    is_return_date = fields.Boolean(string="Return date", default=False)
    student_ids = fields.Many2many('res.partner','book_student_rel','book_history_id','student_id' ,string="Students")
    books_ids = fields.Many2many('library.book','history_book_rel','history_id','book_id',string="Books")
    borrow_request_lines_ids = fields.Many2many('library.borrow.request.line','book_borrow_history_request_rel','book_borrow_history_id','borrow_request_id',string="Borrow Requests Lines")

    # def book_borrow_history(self):
    #     self.ensure_one()
    #     if self.is_return_date:

    # def book_borrow_history(self):
    #     self.ensure_one()
    #     if self.is_return_date:
    #         print("++++++++++++++")
    #         library_borrow_request_line_recs = self.env['library.borrow.request.line'].search([('issue_date','>=',self.start_date),
    #                 ('return_date','<=',self.end_date), ('book_id','in',self.books_ids)])
    #         print("------------------",library_borrow_request_line_recs)
    #         borrow_request_recs = library_borrow_request_line_recs.mapped('borrow_request_id')
    #         print("------------------",borrow_request_recs)
    #         rec = borrow_request_recs.search(
    #             [
    #                 ('student_id', 'in', self.student_ids),
    #             ]
    #         )
    #         self.borrow_request_ids = rec.search(
    #             [
    #                 ('borrow_request_line_ids','in',library_borrow_request_line_recs)
    #             ])
    #
    #         print('')
    #         # self.borrow_request_ids = self.borrow_request_ids.search(
    #         #     [
    #         #         ('borrow_request_line_ids.issue_date','>=',self.start_date),
    #         #         ('borrow_request_line_ids.return_date','<=',self.end_date),
    #         #         ('student_id','in',self.student_ids),
    #         #         ('borrow_request_line_ids.book_id','in',self.books_ids),
    #         #     ]
    #         # )
    #     else:
    #         library_borrow_request_line_rec = self.env['library.borrow.request.line'].search(
    #             [('issue_date', '>=', self.start_date),
    #              ('issue_date', '<=', self.end_date), ('book_id', 'in', self.books_ids)])
    #         borrow_request_recs = library_borrow_request_line_rec.mapped('borrow_request_id')
    #         self.borrow_request_ids = borrow_request_recs.search(
    #             [
    #                 ('student_id', 'in', self.student_ids),
    #             ]
    #         )
    #     return self.env.ref('library_management_man.library_book_borrow_history_report_action').report_action([])

    def book_borrow_history(self):
        self.ensure_one()
        if self.is_return_date:
            self.borrow_request_lines_ids = self.borrow_request_lines_ids.search([
                ('issue_date','>=',self.start_date),
                ('return_date','<=',self.end_date),
                ('borrow_request_id.student_id','in',self.student_ids),
                ('book_id','in',self.books_ids),
            ])
        else:
            self.borrow_request_lines_ids = self.borrow_request_lines_ids.search([
                ('issue_date', '>=', self.start_date),
                ('issue_date', '<=', self.end_date),
                ('borrow_request_id.student_id', 'in', self.student_ids),
                ('book_id', 'in', self.books_ids),
            ])
        return self.env.ref('library_management_man.library_book_borrow_history_report_action').report_action([])

    def borrow_request_cancel_wizard(self):
        self.ensure_one()
        return {
            'type' : 'ir.actions.act_window_close'
        }

    @api.onchange('start_date','end_date')
    def _onchange_start_end_date(self):
        for record in self:
            if record.start_date and record.end_date and record.start_date > record.end_date:
                raise ValidationError("Please enter a valid end date")
