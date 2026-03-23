from odoo.exceptions import ValidationError
from odoo import models,fields,api,_

class LibraryBorrowRequestLines(models.Model):
    _name = 'library.borrow.request.lines'
    _description = 'Library borrow Request Lines'

    book_id = fields.Many2one('library.books', string='Book',required=True)
    quantity = fields.Integer('Quantity',required=True,default=1)
    amount = fields.Float('Amount',compute='_compute_amount')
    issue_date = fields.Date('Issue_date',required=True)
    return_date = fields.Date('Return_date',required=True)
    fine_amount = fields.Float('Fine_Amount') #,compute='_compute_fine_amount'
    total_amount = fields.Float('Total Amount')
    issue_days = fields.Integer('Issue_Days',compute='_compute_issue_days',store=True)
    borrow_request_id = fields.Many2one('library.borrow.requests')
    fine_settings_amt = fields.Integer('Fine_Settings',compute='_compute_fine_amt')

    @api.depends('issue_date','return_date')
    def _compute_issue_days(self):
        for book in self:
            if book.issue_date and book.return_date and (book.return_date - book.issue_date).days>0:
                book.issue_days = (book.return_date - book.issue_date).days
            else:
                book.issue_days = 0
                if book.issue_date and book.return_date and (book.return_date - book.issue_date).days <= 0:
                    raise ValidationError(_("Return date cannot be before Issue date"))

    @api.depends('book_id')
    def _compute_amount(self):
        for book in self:
            book.amount = book.book_id.borrow_price

    def _compute_fine_amt(self):
        fine_amt = self.env['ir.config_parameter'].sudo().get_param('project_management.fine_amount')
        for record in self:
            record.fine_settings_amt = fine_amt

    @api.model_create_multi
    def create(self,vals):
        res = super(LibraryBorrowRequestLines, self).create(vals)
        for rec in res:
            if rec.borrow_request_id and rec.borrow_request_id.state=='issued' and rec.book_id.available_copies - rec.quantity>=0:
                rec.book_id.available_copies -= rec.quantity
        return res