from email.policy import default

from odoo import fields,models,api,_
from odoo.exceptions import ValidationError


class BorrowRequestLines(models.Model):
    _name = 'library.borrow.request.lines'
    _description = 'Borrow Request Lines'
    _rec_name = 'book_id'

    book_id = fields.Many2one('library.books',string='Book',required=True,ondelete='cascade')
    quantity = fields.Integer(string='Quantity',default=1)
    amount_per_unit = fields.Float(string='Amount Per Unit per Day', related='book_id.borrow_price', store=True)
    issue_date = fields.Date(string='Issue Date',required=True)
    return_date = fields.Date(string='Return Date', required=True)
    fine_amount = fields.Float(string='Fine Amount', compute='_compute_fine_amount', store=True)
    total_amount = fields.Float(string='Total Amount', compute='_compute_total_amount', store=True)
    issue_days = fields.Integer(string='Issue Days', compute='_compute_issue_days', store=True)

    borrow_request_id = fields.Many2one('library.borrow.request',string='Borrow Request')

    @api.onchange('issue_date')
    def _onchange_issue_date(self):
        for rec in self:
            if rec.issue_date and rec.return_date:
                if rec.issue_date > rec.return_date:
                    raise ValidationError(_("issue date cannot be greater than return date"))

    @api.onchange('return_date')
    def _onchange_return_date(self):
        self._onchange_issue_date()

    @api.onchange('book_id','quantity')
    def _onchange_book_id(self):
        for rec in self:
            if rec.book_id:
                if rec.quantity > rec.book_id.available_copies:
                    raise ValidationError(_("Insufficient stock"))

    @api.depends('issue_date','return_date')
    def _compute_issue_days(self):
        for rec in self:
            if rec.issue_date and rec.return_date:
                val = (rec.return_date - rec.issue_date).days
                if val >0:
                    rec.issue_days = val
                else:
                    rec.issue_days = 0
                if rec.issue_days > rec.book_id.maximum_day_limit:
                    raise ValidationError(_(f"This book can not be issued beyond {rec.book_id.maximum_day_limit}"))

    @api.depends('return_date','borrow_request_id.return_date')
    def _compute_fine_amount(self):
        for rec in self:
            if rec.borrow_request_id.return_date and rec.return_date:
                fine_amount_config = rec.env['ir.config_parameter'].sudo().get_param('library_management_jui.fine_amount')
                days = rec.borrow_request_id.return_date - rec.return_date
                if days.days > 0:
                    rec.fine_amount = float(fine_amount_config) * days.days
                    self._compute_total_amount()
                    break
                else:
                    rec.fine_amount = 0
                    break

    @api.depends('amount_per_unit','quantity','borrow_request_id.issue_date','return_date')
    def _compute_total_amount(self):
        for rec in self:
            if rec.return_date and rec.borrow_request_id.issue_date:
                issue_d = (rec.return_date - rec.borrow_request_id.issue_date)
                if issue_d.days >= 0:
                    rec.total_amount = (rec.amount_per_unit * rec.quantity * issue_d.days) + rec.fine_amount
                else:
                    rec.total_amount = rec.fine_amount
