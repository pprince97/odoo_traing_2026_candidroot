from odoo import models, fields, api
from datetime import date, timedelta


class BorrowRequestLine(models.Model):
    _name = 'borrow_request_line.borrow_request_line'
    _description = 'Borrow Request Line'

    book_id = fields.Many2one('book.book', string="Book", required=True)
    borrow_id = fields.Many2one('borrow_request.borrow_request', string="Borrow Request", required=True)

    quantity = fields.Integer(string="Quantity", default=1)
    amount_per_unit_per_day = fields.Float(string="Amount Per Unit Per Day")

    issue_date = fields.Date(string="Issue Date")
    return_date = fields.Date(string="Return Date", compute="_compute_return_date")

    issue_days = fields.Integer(string="Issue Days", compute="_compute_issue_days", store=True)

    fine_per_day = fields.Float(string="Fine Per Day", compute="_compute_fine_per_day", store=True)

    fine_amount = fields.Float(string="Fine Amount", compute="_compute_fine_amount")

    total_amount = fields.Float(string="Total Amount", compute="_compute_total_amount", store=True)





    @api.onchange('book_id')
    def _onchange_book_id(self):
        for record in self:
            if record.book_id:
                record.amount_per_unit_per_day = record.book_id.borrow_price_per_day



    @api.depends('issue_date', 'book_id.maximum_day_limit')
    def _compute_return_date(self):
        for record in self:
            if record.issue_date and record.book_id:
                record.return_date = record.issue_date + timedelta(days=record.book_id.maximum_day_limit)
            else:
                record.return_date = False



    @api.depends('issue_date', 'borrow_id.return_date')
    def _compute_issue_days(self):
        for record in self:
            if record.issue_date and record.borrow_id.return_date:
                record.issue_days = (record.borrow_id.return_date - record.issue_date).days
            else:
                record.issue_days = 0

    @api.depends('borrow_id.return_date', 'return_date', 'fine_per_day')
    def _compute_fine_amount(self):
        for record in self:
            record.fine_amount = 0.0

            actual_return = record.borrow_id.return_date
            expected_return = record.return_date

            if actual_return and expected_return:
                if actual_return > expected_return:
                    late_days = (actual_return - expected_return).days
                    record.fine_amount = late_days * record.fine_per_day



    @api.depends('issue_days', 'amount_per_unit_per_day', 'quantity', 'fine_amount')
    def _compute_total_amount(self):
        for record in self:
            amount = record.issue_days * record.amount_per_unit_per_day * record.quantity
            record.total_amount = amount + record.fine_amount