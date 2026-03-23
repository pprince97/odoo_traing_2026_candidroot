from odoo import fields, models, api,_
from odoo.exceptions import ValidationError
from odoo.fields import Domain


class BorrowHistoryWizard(models.TransientModel):
    _name = 'borrow.history.wizard'
    _description = 'Borrow History Wizard'

    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)
    is_return_date = fields.Boolean(string="Return Date")
    students = fields.Many2many('res.partner', 'student_history_rel', 'history_id', 'student_id', string="Students")
    books = fields.Many2many('library.book', 'book_history_rel', 'history_id', 'book_id', string="Books")
    request_ids_ = fields.Many2many('library.borrow.request.line', 'borrow_wizard_rel', 'wizard_id', 'request_id',
                                    string="Requests")

    @api.onchange('start_date')
    def _onchange_start_date(self):
        for rec in self:
            if rec.start_date and rec.end_date and rec.end_date < rec.start_date:
                raise ValidationError(_('start date must be less than end date'))

    @api.onchange('end_date')
    def _onchange_end_date(self):
        for rec in self:
            if rec.end_date and rec.start_date and rec.start_date > rec.end_date:
                raise ValidationError(_('end date must be grater than start date'))

    def checked_wizard_borrow_history(self):
        domain = Domain([('borrow_request_id.return_date', '>=', self.start_date),
                         ('borrow_request_id.return_date', '<=', self.end_date)])
        if self.students and self.books:
            domain &= Domain([('borrow_request_id.student_id', 'in', self.students.ids),
                              ('book_id', 'in', self.books.ids)])
        elif self.students and not self.books:
            domain &= Domain([('borrow_request_id.student_id', 'in', self.students.ids)])
        elif self.books and not self.students:
            domain &= Domain([('book_id', 'in', self.books.ids)])
        return domain

    def unchecked_wizard_borrow_history(self):
        domain = Domain.OR([Domain([('borrow_request_id.return_date', '>=', self.start_date),('borrow_request_id.return_date', '<=', self.end_date)]),
                        Domain([('borrow_request_id.issued_date', '>=', self.start_date),('borrow_request_id.issued_date', '<=', self.end_date)]),
                        Domain([('borrow_request_id.state', '=', 'draft')])])
        if self.students and self.books:
            domain &= Domain([('borrow_request_id.student_id', 'in', self.students.ids),
                              ('book_id', 'in', self.books.ids)])
        elif self.students and not self.books:
            domain &= Domain([('borrow_request_id.student_id', 'in', self.students.ids)])
        elif self.books and not self.students:
            domain &= Domain([('book_id', 'in', self.books.ids)])
        return domain

    def wizard_borrow_history(self):
        self.ensure_one()
        if self.is_return_date:
            domain = self.checked_wizard_borrow_history()
        else:
            domain = self.unchecked_wizard_borrow_history()
        self.request_ids_ = self.env['library.borrow.request.line'].search(domain).ids
        return self.env.ref('library_management_urvi.action_report_library_history').report_action(self.id)

