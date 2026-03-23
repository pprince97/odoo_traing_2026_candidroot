from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class BorrowRequestLines(models.Model):
    _name = 'library.borrow.request.line'
    _description = 'Borrow Request Lines Model'
    _rec_name = 'book_id'

    book_id = fields.Many2one('library.book', string="Book", required=True)
    quantity = fields.Integer(string="Quantity")
    currency_id = fields.Many2one('res.currency', related='book_id.currency_id', string="Currency")
    amount_per_unit = fields.Monetary(string="Amount", help="Amount Per Unit Per Day", currency_field='currency_id',
                                      related="book_id.borrow_price")
    issue_date = fields.Date(string="Issue Date", required=True)
    return_date = fields.Date(string="Return Date", required=True)
    fine_amount = fields.Monetary(string="Fine Amount", currency_field='currency_id', compute="_compute_fine_amount",
                                  store=True)
    total_amount = fields.Monetary(string="Total Amount", currency_field='currency_id', compute='_compute_total_amount',
                                   store=True)
    issue_days = fields.Integer(string="Issue Days",compute='_count_issue_days',store=True)
    borrow_request_id = fields.Many2one('library.borrow.request', string="Borrow Request Lines", ondelete='cascade')

    @api.onchange('issue_date')
    def _onchange_issue_date(self):
        for rec in self:
            if rec.issue_date and rec.return_date and rec.return_date < rec.issue_date:
                raise ValidationError(_('issued date must be less than return date'))
            elif rec.issue_date and rec.return_date and rec.return_date > rec.issue_date:
                pass

    @api.onchange('return_date')
    def _onchange_return_date(self):
        for rec in self:
            if rec.return_date and rec.issue_date and rec.issue_date > rec.return_date:
                raise ValidationError(_('return date must be grater than issue date'))
            elif rec.return_date and rec.issue_date and rec.issue_date < rec.return_date:
                pass

    # check weather issue_days is in limit or not
    @api.depends('issue_date','return_date')
    def _count_issue_days(self):
        for rec in self:
            if rec.issue_date and rec.return_date:
                diff = abs(rec.issue_date - rec.return_date)
                days = diff.total_seconds() // (60 * 60 * 24)
                if days > self.env['library.book'].search([('id', '=', rec.book_id.id)]).maximum_day_limit:
                    raise ValidationError(_('issue days exceed maximum days limit'))
                else:
                    rec.issue_days = days

    # check weather stock is available or not
    @api.onchange('quantity')
    def _onchange_quantity(self):
        for rec in self:
            rec.book_id._compute_available()
            if rec.quantity and rec.quantity > self.env['library.book'].search([('id', '=', rec.book_id.id)]).available:
                raise ValidationError(_('BOOK OUT OF STOCK:quantity exceed available limit of book'))

    @api.depends('borrow_request_id.return_date')
    def _compute_fine_amount(self):
        fine = self.env['ir.config_parameter'].get_param('project_management_urvi.fine_amount')
        if fine:
            for rec in self:
                if rec and rec.borrow_request_id.return_date > rec.return_date:
                    print('>>>>>>>>>>>>>>>>>', fine, rec.quantity, (rec.borrow_request_id.days - rec.issue_days))
                    rec.fine_amount = float(fine) * rec.quantity * (rec.borrow_request_id.days - rec.issue_days)

    @api.depends('issue_days', 'fine_amount', 'quantity')
    def _compute_total_amount(self):
        for rec in self:
            if rec:
                rec.total_amount = rec.fine_amount + (rec.quantity * rec.amount_per_unit * rec.issue_days)

    @api.model_create_multi
    def create(self, vals):
        res = super(BorrowRequestLines, self).create(vals)
        return res

