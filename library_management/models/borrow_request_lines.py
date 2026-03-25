from dateutil.relativedelta import relativedelta
from odoo import fields, models, api
from datetime import date
from odoo.exceptions import ValidationError


class BorrowRequest(models.Model):
    _name = 'borrow.requestline'
    _description = 'Borrow Request Line'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'book_id'

    book_id = fields.Many2one('library.books', string='Book')
    quantity = fields.Integer(string='Quantity', default=1)
    amount_per_day = fields.Float(string='Amount Per Day')

    borrow_request_id = fields.Many2one('library.borrow.request', string='Borrow Request')
    issue_date = fields.Date(string='Issued Date', readonly=True)  # , compute='_compute_issue_date'
    return_date = fields.Date(string='Return Date', readonly=True)
    fine_amount = fields.Float(string='Fine Amount')  # ,compute='_fine_amount'
    fine_per_day = fields.Float(string='Fine Per Day', compute='_fine_amount_per_day')
    total_amount = fields.Float(string='Total Amount')
    issue_days = fields.Integer(string='Issued Days')
    due_days = fields.Integer(string='Due Days', compute='_due_days')

    # @api.depends('borrow_request_id.state')
    # def _compute_issue_date(self):
    #     for rec in self:
    #         if rec and rec.borrow_request_id and rec.borrow_request_id.state == 'issue':
    #             rec.issue_date = date.today()
    #         else:
    #             rec.issue_date = None

    @api.onchange('book_id')
    def _amount_per_day(self):
        for doc in self:
            doc.amount_per_day = doc.book_id.borrow_price


    @api.onchange('quantity')
    def _onchange_quantity(self):
        for doc in self:
            if doc.quantity < 1:
                doc.quantity = 1
                raise ValidationError("Quantity is less than 1.")


    @api.onchange('issue_date', 'borrow_request_id.state')
    def _onchange_date(self):
        for doc in self:
            return_days = doc.book_id.maximum_day_limit
            print("return_days", return_days, doc.book_id.maximum_day_limit)
            if doc.issue_date:
                doc.return_date = (doc.issue_date + relativedelta(days=return_days)).date()
                print(doc.return_date, "\n\n")


    def _due_days(self):
        for doc in self:
            today = date.today()
            if today < doc.return_date:
                doc.due_days = 0
            else:
                doc.due_days = (today - doc.return_date).days


    def _fine_amount_per_day(self):
        for doc in self:
            print("\n\n", doc.fine_per_day)
            if self.env['ir.config_parameter'].sudo().get_param('is_active_fine'):
                doc.fine_per_day = self.env['res.config.settings'].fine_per_day_
                print("\n\n", doc.fine_per_day)
            else:
                doc.fine_per_day = 0
                print("\n\n", doc.fine_per_day)


# def _fine_amount(self):
#     for doc in self:
#         print(doc.fine_per_day,doc.due_days)
#         doc.fine_amount = (doc.fine_per_day * doc.due_days)
#         print(doc.fine_amount)


# @api.onchange('issue_date','return_date','quantity','book_id')
# def _total_amount(self):
#     for doc in self:
#         doc.total_amount = (doc.quantity * doc.issue_days * doc.amount_per_day) + (doc.fine_per_day * doc.due_days)


# Fields:
# Book(required)
# Quantity
# Amount Per Unit Per Day(Auto Calculate From Book)
# Issue Date(required)
# Return Date(required)
# Fine Amount(Auto Calculate From The Delayed Return Days Per day Amount will be Added )
# Total Amount(Auto Calculated From the Per Day Amount, Quantity Plus added Fine Amount )
# Issue Days(Auto Calculate From Return Date and Issue Date)
# Business Rules:
# ● Validation Days of issue can not be more than Configured Day Limit from Book
