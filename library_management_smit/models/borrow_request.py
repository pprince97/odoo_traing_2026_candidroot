from odoo import models, fields, api
from datetime import date
from odoo.exceptions import ValidationError


class LibraryBookBorrow(models.Model):
    _name = 'library.book.borrow'
    _description = 'Book Borrow'

    serial_number = fields.Char(string='Serial Number')
    student_id = fields.Many2one('res.users', string='Student')
    librarian_id = fields.Many2one('res.users', string='Librarian', readonly=True, default=lambda self: self.env.user)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('issued', 'Issued'),
        ('returned', 'Returned'),
        ('cancelled', 'Cancelled'),
    ], string='State', default='draft')
    return_date = fields.Date(string='Returned Date', readonly=True)
    issue_date = fields.Date(string='Issued Date', readonly=True)
    fine_amount = fields.Float(string='Fine Amount', compute='_compute_fine_amount')
    total_amount = fields.Float(string='Total Amount', compute='_compute_total_amount')
    cancelled_date = fields.Date(string='Cancelled Date', readonly=True)
    cancellation_reason = fields.Char(string='Cancellation Reason')
    borrow_req_ids = fields.One2many('library.book.borrow.lines', 'borrow_req_id',
                                     string='Borrow Requests')
    extra_days = fields.Integer(string='Extra Days', compute='_compute_extra_days')

    @api.depends('issue_date', 'return_date')
    def _compute_extra_days(self):
        for rec in self:
            rec.extra_days = 0

    @api.depends('borrow_req_ids')
    def _compute_fine_amount(self):
        for rec in self:
            rec.fine_amount = sum(rec.borrow_req_ids.mapped('fine_amount_book'))

    @api.depends('borrow_req_ids')
    def _compute_total_amount(self):
        for rec in self:
            rec.total_amount = sum(rec.borrow_req_ids.mapped('total_amount'))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['serial_number'] = self.env['ir.sequence'].next_by_code('borrow.sequence')
        return super().create(vals_list)

    def action_issue_books(self):
        for rec in self:
            rec.update({"state": "issued"})
            rec.issue_date = date.today()

            for line in rec.borrow_req_ids:
                line.book_id._compute_available_copies_count()
                if line.book_id.available_copies< 0:
                    rec.update({"state": "draft"})
                    raise ValidationError(f'Book {line.book_id.name} quantity exceeds available copies!')

    def action_return_books(self):
        self.update({"state": "draft"})
        for rec in self:
            rec.return_date = date.today()

    def action_cancel_books(self):
        self.update({"state": "draft"})
        for rec in self:
            rec.cancelled_date = date.today()

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'cancellation.wizard',
            'view_mode': 'form',
            'context': {'borrow_request': self.id},
            'target': 'new'
        }
