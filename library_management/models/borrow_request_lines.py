from odoo import fields, models, api
from odoo.exceptions import ValidationError


class BorrowRequestLine(models.Model):
    _name = 'borrow.request.line'
    _description = 'Borrow Request Line'

    book_id = fields.Many2one('library.books', string='Book')
    quantity = fields.Integer(string='Quantity')

    amount_per_day = fields.Float(string='Per Unit Amount', related='book_id.borrow_price')

    issue_date = fields.Datetime(string='Issue Date', required=True)
    return_date = fields.Datetime(string='Return Date', required=True)

    fine_amount = fields.Float(string='Fine Amount')
    total_amount = fields.Float(string='Total Amount')


    issue_days = fields.Integer(string='Issue Days')


    # Relation
    borrow_request_id = fields.Many2one('library.borrow.request', string='Borrow Requests')

    student_id = fields.Many2one('res.partner', string='Student', domain=[('member', '=', 'student')])

    @api.onchange('issue_date','return_date')
    def _onchange_days(self):
        if self.issue_date and self.return_date:
            if self.issue_date > self.return_date:
                raise ValidationError("issue_date must be before return_date")
            else:
                res = ((self.return_date - self.issue_date).total_seconds()) / 86400
                self.issue_days = res

    @api.onchange('issue_days', 'quantity')
    def _onchange_amount(self):
        if self.issue_days <= self.book_id.maximum_day_limit:
            self.fine_amount = 0
        else:
            delayed_days = self.issue_days - self.book_id.maximum_day_limit
            self.fine_amount = delayed_days * self.book_id.fine_amount * self.quantity

    @api.onchange('issue_days', 'fine_amount', 'quantity')
    def _onchange_total_amount(self):
        self.total_amount = (self.quantity * self.amount_per_day * self.issue_days) + self.fine_amount


    # Check Quantity
    @api.onchange('book_id')
    def _compute_quantity(self):
        for rec in self:
            if rec.quantity and rec.quantity > rec.book_id.available_copies:
                raise ValidationError(f"Only {rec.book_id.available_copies} copies of the {rec.book_id.name} are available")
