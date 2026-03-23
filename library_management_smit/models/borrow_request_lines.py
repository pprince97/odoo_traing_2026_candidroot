from odoo import models, fields, api
from odoo.exceptions import ValidationError

class LibraryBookBorrowLines(models.Model):
    _name = 'library.book.borrow.lines'
    _description = 'Book Borrow Line'
    _rec_name = 'book_id'
    _order = 'sequence'

    sequence = fields.Integer(string='Sequence')
    borrow_req_id = fields.Many2one('library.book.borrow', string='Borrow Request')
    book_id = fields.Many2one('library.book', string='Book', required=True)
    quantity = fields.Integer(string='Quantity', default=1)
    amount_per_day = fields.Float(string='Amount Per Day', compute='_compute_amount_per_day')
    issue_date_book = fields.Date(string='Issued Date')
    return_date_book = fields.Date(string='Returned Date')
    fine_amount_book = fields.Float(string='Fine Amount Per Book', compute='_compute_fine_amount_book')
    total_amount = fields.Float(string='Total Amount', compute='_compute_total_amount')
    issue_days = fields.Integer(string='Issued Days', compute='_compute_issue_days')

    @api.onchange('quantity','book_id')
    def _onchange_quantity(self):
        for rec in self:
            if rec.book_id:
                if (rec.book_id.available_copies < rec.quantity) or (rec.quantity< 1):
                    rec.book_id._compute_available_copies_count()
                    raise ValidationError("Invalid Quantity!")

    @api.depends('borrow_req_id', 'book_id')
    def _compute_amount_per_day(self):
        for rec in self:
            rec.amount_per_day = rec.book_id.borrow_price

    @api.depends('return_date_book', 'issue_date_book')
    def _compute_issue_days(self):
        for day in self:
            if day.issue_date_book and day.return_date_book and (day.return_date_book - day.issue_date_book).days > 0:
                day.issue_days = (day.return_date_book - day.issue_date_book).days
                if (day.issue_days < 0) or (day.issue_days > day.book_id.max_day_limit):
                    raise ValidationError("Invalid Return Date!")

            else:
                day.issue_days = 0

    @api.depends('borrow_req_id.return_date')
    def _compute_fine_amount_book(self):
        for rec in self:
            if rec.borrow_req_id.return_date and rec.return_date_book:
                extra_days = rec.borrow_req_id.return_date - rec.return_date_book

                if extra_days.total_seconds() > 0:
                    rec.fine_amount_book = (extra_days.total_seconds() / 86400) * rec.quantity * rec.book_id.fine_amount
                else:
                    rec.fine_amount_book = 0
            else:
                rec.fine_amount_book = 0

    @api.depends('fine_amount_book')
    def _compute_total_amount(self):
        for rec in self:
            rec.total_amount = (rec.amount_per_day * rec.quantity * rec.issue_days) + rec.fine_amount_book


