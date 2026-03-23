from odoo import models,fields,api,_
from odoo.exceptions import ValidationError

class BorrowRequestLines(models.Model):
    _name = 'library.borrow.request.lines'
    _description = 'Library Borrow Request Lines'

    book_id = fields.Many2one('library.books',string='Book',required=True,domain="[('state','=','published')]")
    quantity = fields.Integer(string='Quantity')
    amount = fields.Float(string='Amount',compute='_compute_amount')
    issue_date = fields.Date(string='Issue Date',required=True)
    return_date = fields.Date(string='Return Date',required=True)
    fine_amount = fields.Float(string='Fine Amount')
    total_amount = fields.Float(string='Total Amount',compute='_compute_total_amount')
    issue_days = fields.Integer(string='Issue Days',compute='_compute_issue_days')
    borrow_request_id = fields.Many2one('library.borrow.request',string='Borrow Request')

    # fine_amount_config = fields.Float(string="Fine Amount Config",compute="_compute_fine_amount_config")


    @api.depends('issue_date','return_date')
    def _compute_issue_days(self):
        for rec in self:
            if rec.issue_date and rec.return_date:
                rec.issue_days = (rec.return_date-rec.issue_date).days
            else:
                rec.issue_days = 0

    @api.depends('book_id')
    def _compute_amount(self):
        for rec in self:
            if rec.book_id:
                rec.amount = rec.book_id.borrow_price
            else:
                rec.amount = 0

    # def _compute_fine_amount_config(self):
    #     show_amount = self.env['ir.config_parameter'].sudo().get_param('library_management.fine_amount_per_dayy')
    #     for rec in self:
    #         rec.fine_amount_config = show_amount
    #
    # @api.depends('issue_days','book_id','fine_amount_config')
    # def _compute_fine_amount(self):
    #     for rec in self:
    #         if rec.issue_days and rec.issue_days > rec.book_id.maximum_day:
    #             difference = rec.issue_days - rec.book_id.maximum_day
    #             rec.fine_amount = rec.fine_amount_config * difference
    #         else:
    #             rec.fine_amount = 0
    #
    @api.depends('amount','quantity')
    def _compute_total_amount(self):
        for rec in self:
            if rec.amount:
                rec.total_amount = rec.amount*rec.quantity
            else:
                rec.total_amount = 0

    @api.onchange('issue_date')
    def _onchange_issue_date(self):
        for rec in self:
            if rec.issue_date and rec.return_date and rec.issue_date >rec.return_date:
                raise ValidationError(_('Issued date cannot be greater than Returned date'))

    @api.onchange('return_date')
    def _onchange_return_date(self):
        for rec in self:
            if  rec.issue_date and rec.return_date and rec.issue_date > rec.return_date:
                raise ValidationError(_('Returned date cannot be lesser than Issued date'))
            if rec.book_id and rec.issue_days > rec.book_id.maximum_day:
                raise ValidationError(_('Maximum day limit reached'))

    @api.model_create_multi
    def create(self, vals):
        res = super(BorrowRequestLines,self).create(vals)
        for rec in res:
            if rec.book_id and rec.borrow_request_id.state == 'issued' and rec.book_id.available_copies - rec.quantity >= 0 :
                rec.book_id.available_copies -= rec.quantity
        return res
