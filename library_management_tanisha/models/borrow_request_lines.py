from odoo import models,fields,api,_

from odoo.exceptions import ValidationError


class LibraryBorrowRequestLines(models.Model):
    _name = 'library.borrow.request.lines'
    _description = 'Borrow Request Lines'
    _rec_name = 'book_id'

    book_id = fields.Many2one(comodel_name='library.book',string='Book',required=True)
    quantity = fields.Integer(string='Quantity')
    amount_per_unit_per_day = fields.Float(compute='_compute_amount_per_day',string='Amount per unit per day')
    issue_date = fields.Date(string='Issue date',required=True)
    return_date = fields.Date(string='Return date',required=True)
    issue_days = fields.Integer(string='Issue days',compute='_compute_issue_days')
    fine_amount = fields.Float(string='Fine amount')
    total_amount = fields.Float(string='Total amount',compute='_compute_total_amount')
    borrow_request_id = fields.Many2one(comodel_name='library.borrow.request',string='Borrow Request')
    borrow_history_ids = fields.Many2many(comodel_name='book.history.wizard', relation='borrow_history_request_line_rel', column1='request_line_id',column2='book_borrow_id', string='Books History')

    @api.depends('book_id')
    def _compute_amount_per_day(self):
        for book in self:
            book.amount_per_unit_per_day = book.book_id.borrow_price

    @api.depends('issue_date','return_date')
    def _compute_issue_days(self):
        for book in self:
            if book.issue_date and book.return_date:
                book.issue_days = (book.return_date - book.issue_date).days
            else:
                book.issue_days = 0

    @api.onchange('return_date','issue_date')
    def _onchange_return_date(self):
        for book in self:
            if book.return_date:
                if book.issue_days > book.book_id.max_day_limit:
                    raise ValidationError(_("Return date is greater than max day limit!!!!"))

    @api.depends('amount_per_unit_per_day')
    def _compute_total_amount(self):
        for book in self:
            book.total_amount = book.amount_per_unit_per_day * book.quantity + book.fine_amount

    @api.onchange('quantity')
    def _onchange_quantity(self):
        for book in self:
            if book.book_id and book.quantity>book.book_id.available_copies:
                raise ValidationError(_("Books out of stock!!!!"))
