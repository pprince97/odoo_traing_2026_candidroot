
from odoo import models, fields, api

class LibraryBorrowRequestLine(models.Model):
    _name = 'library.borrow.request.line'
    _description = 'Library Borrow Request Line'

    book_id = fields.Many2one('library.book',string='Book',required=True)
    quantity = fields.Integer('Quantity')
    amount_per_unit = fields.Float('Amount Per Unit')
    issue_date = fields.Date('Issued Date',required=True)
    return_date = fields.Date('Return Date',required=True)
    fine_amount = fields.Float('Fine Amount')
    total_amount = fields.Float('Total Amount')
    issue_days = fields.Integer('Issued Days')
    borrow_request_id = fields.Many2one('library.borrow.request')
    student_id = fields.Many2one('res.partner', related='borrow_request_id.student_id' )

    @api.onchange('book_id', 'return_date', 'issue_date','quantity')
    def _onchange_borrow_line(self):
        if self.book_id:
            self.amount_per_unit = self.book_id.borrow_price

        if self.return_date and self.issue_date:
            self.issue_days = (self.return_date - self.issue_date).days

        if self.issue_days and self.issue_days > self.book_id.maximum_day_limit:
            self.fine_amount = (self.issue_days - self.book_id.maximum_day_limit) * self.book_id.fine_amount * self.quantity
            self.total_amount = (self.amount_per_unit * self.book_id.maximum_day_limit) + self.fine_amount
        else:
            self.fine_amount = 0
            self.total_amount = (self.issue_days * self.amount_per_unit) + self.fine_amount





